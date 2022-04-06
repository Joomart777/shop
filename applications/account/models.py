from django.contrib.auth.base_user import BaseUserManager
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class UserManager(BaseUserManager):
 def _create_user(self, email, password, **extra_fields):  # Создание юзера -- Скопирнули с встроенного с Джанго методы создания юзеров, корректнули

    if not email:
        raise ValueError("The given email must be set")
    email = self.normalize_email(email)
    user = self.model( email=email, **extra_fields)
    user.create_activation_code()  # При создании юзера, активируем подтверждение по почте
    user.set_password(password)
    user.save(using=self._db)
    return user


 def create_user(self, email, password, **extra_fields):
    extra_fields.setdefault("is_staff", False)
    extra_fields.setdefault("is_superuser", False)
    return self._create_user(email, password, **extra_fields)


 def create_superuser(self, email, password, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)
    extra_fields.setdefault("is_active", True)
    # Активный пользователь, сможет все делать

    if extra_fields.get("is_staff") is not True:
        raise ValueError("Superuser must have is_staff=True.")
    if extra_fields.get("is_superuser") is not True:
        raise ValueError("Superuser must have is_superuser=True.")

    return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=100, blank=True) ## активационный код на почту
    objects = UserManager() # Переопределили класс ВЫше

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4()) #рандомно сгенерировался
        self.activation_code = code


