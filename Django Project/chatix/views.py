from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate
from .models import UserInfo, ChatRoom , Message
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

# Create your views here.


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        image = request.FILES.get('image',)
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        user= User.objects.create_user(username=username, password=password)
        user_info = UserInfo.objects.create(user=user,name=name,email=email,phone=phone,image=image)
        user.save()
        user_info.save()
        login(request,user=user)
        messages.success(request, 'Registration successful')
        return redirect('login')
    
    return render(request, 'chatix/register.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user=authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request,'chatix/login.html')


@login_required
def index(request):
    chatrooms = ChatRoom.objects.filter(participants=request.user)
    return render(request, 'chatix/index.html', {'chatrooms': chatrooms})


@login_required
def search(request):
    query = request.GET.get('q', '')
    users = []

    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(userinfo__name__icontains=query) |
            Q(userinfo__email__icontains=query)
        ).distinct().exclude(id=request.user.id)  # Exclude the current user

    return render(request, 'chatix/search.html', {'query': query, 'users': users})


def chatroom(request,id):
    room = get_object_or_404(ChatRoom, id=id)

    if request.user not in room.participants.all():
        return redirect('index')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(chatroom=room, sender=request.user, content=content)
            return redirect('chatroom', id=id)
            
    messages = room.messages.all()
    return render(request, 'chatix/chatroom.html', {'room': room, 'messages': messages})

def add_user_to_chatroom(request, user_id):
    receiver = User.objects.get(id=user_id)
    sender = request.user

    if sender == receiver:
        messages.error(request, "You cannot chat with yourself.")
        return redirect('index')

    chatroom = ChatRoom.objects.filter(participants=sender).filter(participants=receiver).first()

    if not chatroom:
        name=f"{sender.username}---{receiver.username}"
        chatroom = ChatRoom.objects.create(name=name)
        chatroom.participants.add(sender, receiver)
        chatroom.save()

    return redirect('chatroom',id=chatroom.id)

@login_required
def delete_chatroom(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    
    # Optional: Only allow delete if user is a participant or admin
    if request.user in room.participants.all() or request.user.is_superuser:
        room.delete()
        return redirect('index')  # Or wherever you want to redirect
    else:
        return HttpResponseForbidden("You are not allowed to delete this room.")
    
@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # Only allow sender or admin to delete
    if request.user == message.sender or request.user.is_superuser:
        room_id = message.room.id
        message.delete()
        return redirect('chatroom', room_id=room_id)
    else:
        return HttpResponseForbidden("You are not allowed to delete this message.")