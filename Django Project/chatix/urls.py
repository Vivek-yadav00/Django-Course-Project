from django.contrib import admin
from django.urls import path,include
from django.conf import settings        
from django.conf.urls.static import static
from .views import Login, register,search, index, chatroom,add_user_to_chatroom, delete_chatroom, delete_message

urlpatterns = [
    path('', register, name="home"),
    path('register/', register, name="register"),
    path('login/', Login, name="login"),
    path('index/', index, name="index"),
    path('search/', search, name="search"),
    path('chatroom/<int:id>/', chatroom, name="chatroom"),
    path('add_user_to_chatroom/<int:user_id>/', add_user_to_chatroom, name="add_user_to_chatroom"),
    path('room/delete/<int:room_id>/', delete_chatroom, name='delete_chatroom'),
    path('message/delete/<int:message_id>/', delete_message, name='delete_message'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)