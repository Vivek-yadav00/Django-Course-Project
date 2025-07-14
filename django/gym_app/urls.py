from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views
from .views import fun, allmembers, add_member, delete, register,reminder

urlpatterns = [
    path('', allmembers, name="index"),
    path('add/', add_member, name="adding"),
    path('delete/<int:id>/', delete, name="delete_member"),
    path('login/', views.LoginView.as_view(template_name="gym_app/login.html"), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
    path('send_reminder/', reminder, name='reminder')
]
