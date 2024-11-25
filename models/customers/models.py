from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from models.base import BaseModel

class CustomerManager(BaseUserManager):
  def create_user(self, email, password=None, **extra_fields):
    if not email:
        raise ValueError('The Email field must be set')
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    return self.create_user(email, password, **extra_fields)

class Customer(AbstractUser, BaseModel):
  username = None
  email = models.EmailField(_('email address'), unique=True)
  phone = models.CharField(max_length=20, blank=True)
  country = models.CharField(max_length=2, blank=True)
  status = models.CharField(
    max_length=20,
    choices=[
      ('active', 'Active'),
      ('inactive', 'Inactive'),
      ('suspended', 'Suspended')
    ],
    default='active'
  )

  objects = CustomerManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name']

  class Meta:
    app_label = 'models'
    db_table = 'customers'