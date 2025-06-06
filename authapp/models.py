from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")

        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):

    UserRole=(
        {
            "Admin":"ADMIN",
            "Buyer":"BUYER",
            "Seller":"SELLER"
        }
    )
    email = models.EmailField(unique = True,max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null = True)
    phone_number = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='profile_pics/',blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    role = models.CharField(max_length=6, choices=UserRole, default='Buyer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'