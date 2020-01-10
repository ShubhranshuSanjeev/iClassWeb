from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import Student, Teacher, User

class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model                   = User
        fields                  = ('email', 'username', 'password1', 'password2')
    
    def clean_email(self):
        email                   = self.cleaned_data.get('email')
        qs                      = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is Taken")
        return email

    def clean_username(self):
        username                = self.cleaned_data.get('username')
        qs                      = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean_password2(self):
        password1               = self.cleaned_data.get("password1")
        password2               = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    @transaction.atomic
    def save(self, commit=True):
        user                    = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_student         = True
        user.save()
        student                 = Student.objects.create(username=user)
        return user

class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model                   = User
        fields                  = ('email', 'username', 'password1', 'password2')
    
    def clean_email(self):
        email                   = self.cleaned_data.get('email')
        qs                      = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email is Taken")
        return email

    def clean_username(self):
        username                = self.cleaned_data.get('username')
        qs                      = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean_password2(self):
        password1               = self.cleaned_data.get("password1")
        password2               = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    @transaction.atomic
    def save(self, commit=True):
        user                    = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_teacher         = True
        user.save()
        teacher                 = Teacher.objects.create(username=user)
        return user