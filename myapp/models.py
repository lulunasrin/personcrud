
from django.db import models

class Person(models.Model):
    # Fields for Person
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name  # Provides a readable string representation of the object

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserNewManager(BaseUserManager):
 def create_user(self, email, password=None, name=None, phone=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not name:
            raise ValueError('The Name field must be set')
        if not phone:
            raise ValueError('The Phone field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
class UserNew(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)
    
    # Additional fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserNewManager()

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = ['name']  # Fields required when creating a user

    def __str__(self):
        return self.email
