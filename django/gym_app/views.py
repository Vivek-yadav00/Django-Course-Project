from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import Member,Contact
from .form import MemberForm,ContactForm
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


# Create your views here.
def fun(request):
    return HttpResponse("Hello World")


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('index')
        else:
            return render(request,'gym_app/register.html',{"form":form})
            
    else:
        register_form=UserCreationForm()
        return render(request,'gym_app/register.html',{"form":register_form})


# member=[{"name":"Vivek","age":21}]
@login_required
def allmembers(request):
    show_expired = request.GET.get("show") == "expired"
    if show_expired:
        member = Member.objects.select_related("contact").filter(user=request.user, expiry_date__lt=now().date())
    else:
        member = Member.objects.select_related("contact").filter(user=request.user)

    return render(request, 'gym_app/app.html', {'member': member, 'show_expired': show_expired})

@login_required
def reminder(request):
        member = Member.objects.select_related("contact").filter(user=request.user, expiry_date__lt=now().date())
        for i in member:
            send_mail(subject="Membership expired -- Renewal Reminder",message="Please renew your plan",from_email=None,recipient_list=[i.contact.email],fail_silently=False)
        return redirect('index')



# def add_member(request):
#     if request.method=="POST":
#         name=request.POST["name"]
#         age=int(request.POST["age"])
#         email=request.POST["email"]
#         phone=int(request.POST["phone"])
#         join_date=now().date()
#         expiry_date=join_date+timedelta(days=180)
#         contact=Contact(email=email,phone=phone)
#         member=Member(user=request.user,contact=contact,name=name,age=age,join_date=join_date,expiry_date=expiry_date)
#         member.save()
#         contact.save()
#         return redirect("index")
#     return render(request,'gym_app/add_members.html')

@login_required
def add_member(request):
    if request.method == "POST":
        member_form = MemberForm(request.POST)
        contact_form = ContactForm(request.POST)

        if member_form.is_valid() and contact_form.is_valid():
            contact = contact_form.save()
            member = member_form.save(commit=False)
            member.user = request.user
            member.join_date = now().date()
            member.expiry_date = member.join_date + timedelta(days=180)
            member.contact = contact
            member.save()
            return redirect("index")
        else:
            # Return form with errors
            return render(request, 'gym_app/add_members.html', {"member_form": member_form,"contact_form": contact_form})
    else:
        member_form = MemberForm()
        contact_form = ContactForm()
        return render(request, 'gym_app/add_members.html', {
            "member_form": member_form,
            "contact_form": contact_form
        })


def delete(request ,id):
    member=get_object_or_404(Member,id=id)
    member.delete()
    return redirect("index")