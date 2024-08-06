from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    
    email = models.EmailField(unique=True)
    emp_id = models.CharField(max_length=100, unique=True, default='UNKNOWN')
    profile_pic = models.ImageField("p_img", blank=True, null = True)
    phone_no = models.CharField(max_length=10,  blank=True, null = True)
    address = models.CharField(max_length=100,  blank=True, null = True)
    role = models.CharField(max_length=50,  blank=True, null = True)
    bio = models.TextField( blank=True, null = True)


    USERNAME_FIELD = ("email")
    REQUIRED_FIELDS = ("username",)

    def __str__(self):
        return self.email

class EmpID(models.Model):
    emp_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.emp_id