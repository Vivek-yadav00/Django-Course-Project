from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Contact(models.Model):
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=10,  unique=True)
    def __str__(self):
        return self.email
    

class Member(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    contact=models.OneToOneField(Contact,on_delete=models.CASCADE)
    name= models.CharField(max_length=200)
    age=models.IntegerField()
    join_date=models.DateField()
    expiry_date=models.DateField()
    def __str__(self):
        return self.name
