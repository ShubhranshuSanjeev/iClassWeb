from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.postgres.fields import ArrayField

from .managers import CustomUserManager

class User(AbstractBaseUser):
    username            = models.CharField(max_length = 30, primary_key = True)
    email               = models.EmailField(verbose_name="Email", max_length = 60, unique=True)
    first_name          = models.CharField(verbose_name="First name", max_length=30, blank=True)
    last_name           = models.CharField(verbose_name="Last name", max_length=30, blank=True)
    # avatar            = models.ImageField(upload_to='userProfilePic/')
    
    date_joined         = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_active           = models.BooleanField(verbose_name="active", default=True)
    
    is_student          = models.BooleanField(default=False)
    is_teacher          = models.BooleanField(default=False)

    USERNAME_FIELD      = 'email'
    REQUIRED_FIELDS     = [username, is_student, is_teacher,]

    objects = CustomUserManager()

    def __str__(self):
        return self.username + " " +self.email

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name
    
    def get_user(self):
        return self
    

class Student(models.Model):
    username            = models.OneToOneField(User, on_delete = models.CASCADE, primary_key=True)

    def get_user(self):
        return self

class Teacher(models.Model):
    username            = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def get_user(self):
        return self