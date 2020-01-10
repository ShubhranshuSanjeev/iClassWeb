from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView, UpdateView

from .forms import StudentSignUpForm, TeacherSignUpForm
from .models import User

def index(request):
    return render(request, 'base.html')

class SignupView(TemplateView):
    template_name               = 'accounts/signup.html'

class UserProfileView(TemplateView):
    template_name               = 'accounts/profile.html'

class TeacherSignUpView(CreateView):
    model                       = User
    form_class                  = TeacherSignUpForm
    template_name               = 'accounts/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type']     = 'Teacher'
        return super().get_context_data(**kwargs)
        
    def form_valid(self, form):
        user                    = form.save()
        login(self.request, user)
        return redirect('index')

class StudentSignUpView(CreateView):
    model                       = User
    form_class                  = StudentSignUpForm
    template_name               = 'accounts/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type']     = 'Student'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user                    = form.save()
        login(self.request, user)
        return redirect('index')

class ProfileUpdate(UpdateView):
    model                       = User
    fields                      = ['email', 'first_name', 'last_name']
    template_name_suffix        = '_update_form'
    success_url                 = '../profile'
    def get_object(self):
        return self.request.user
