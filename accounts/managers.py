from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, username, is_student, is_teacher, **extra_fields):
        if not email:
            raise ValueError(_("The email value must be set"))
        if not username:
            raise ValueError(_("Username must be provided"))
        if not password:
            raise ValueError(_("Password must be set"))
        
        email               = self.normalize_email(email)
        user                = self.model(email=email, username=username, is_student=is_student, is_teacher=is_teacher, **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_user(self, email, password=None, username=None, is_student=False, is_teacher=False, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, username, is_student, is_teacher, **extra_fields)

    def create_superuser(self, email, password=None, username=None, is_student=False, is_teacher=False, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is False:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self._create_user(email, password, username, is_student, is_teacher, **extra_fields)