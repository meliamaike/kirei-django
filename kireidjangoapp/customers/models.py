from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _



class CustomerManager(BaseUserManager):
    # customer = user
    def create_user(self, email, password, first_name, last_name, document_number, area_code, phone_number, is_admin, is_active, is_staff, is_superuser):
        if not email:
            raise ValueError("Debe ingresar un email.")
        user = self.model(
        email=self.normalize_email(email),
        first_name=first_name,
        last_name=last_name,
        document_number=document_number,
        area_code=area_code,
        phone_number=phone_number,
        is_admin=is_admin,
        is_active=is_active,
        is_staff=is_staff,
        is_superuser=is_superuser,
    )
        # user.password = make_password("meliama95")
        user.my_set_password(raw_password=password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            #username=username,
            **extra_fields
        )
        user.my_set_password(raw_password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class Customer(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    document_number = models.CharField(max_length=30)
    email = models.EmailField(max_length=255, unique=True)
    area_code = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=25)
    password = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "document_number",
        "area_code",
        "phone_number",
    ]

    objects = CustomerManager()

    def __str__(self):
        return self.email

    
