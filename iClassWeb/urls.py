"""iClassWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from accounts import views as accountViews
from classroom import views as classroomViews
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accountViews.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), {'next':'accounts/'} , name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', accountViews.SignupView.as_view(), name='signup'),
    path('signup/teacher', accountViews.TeacherSignUpView.as_view(), name='teacher_signup'),
    path('signup/student', accountViews.StudentSignUpView.as_view(), name='student_signup'),
    path('profile/', accountViews.UserProfileView.as_view(), name='user_profile'),
    path('update_profile/', accountViews.ProfileUpdate.as_view(), name='user_profile_update'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name='reset_password'),
    path('dashboard/', classroomViews.Dashboard.as_view(), name='dashboard'),
    path('create_class/', classroomViews.CreateClassRoom.as_view(), name='create_class'),
    path('join_class/', classroomViews.JoinClassRoom.as_view(), name='join_class'),
    path('list_classrooms/', classroomViews.ListClassRooms.as_view(), name='list_classrooms'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    re_path(r'^view_classrooms/(?P<pk>[0-9A-Za-z_\-]+)/$', classroomViews.ClassRoomDetails.as_view(), name='view_classroom'),
    re_path(r'^list_submissions/(?P<pk>[0-9]+)/$', classroomViews.ListAssignmentSubmissions.as_view(), name='list_submissions'),
    re_path(r'^update_marks/(?P<pk>[0-9]+)/$', classroomViews.UpdateMarksView.as_view(), name='update_marks'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
