from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from PIL.Image import Image
import logging
import mimetypes




class CustomerManager(BaseUserManager):
    # customer = user
    def create_user(self, email, username, password, first_name, last_name, document_type, document_number, country_code, area_code, phone_number, profile_image, is_admin, is_active, is_staff, is_superuser):
        if not email:
            raise ValueError("Debe ingresar un email.")
        if not username:
            raise ValueError("Debe ingresar un nombre de usuario.")
        user = self.model(
        email=self.normalize_email(email),
        username=username,
        first_name=first_name,
        last_name=last_name,
        document_type=document_type,
        document_number=document_number,
        country_code=country_code,
        area_code=area_code,
        phone_number=phone_number,
        profile_image=profile_image,
        is_admin=is_admin,
        is_active=is_active,
        is_staff=is_staff,
        is_superuser=is_superuser,
    )
        # user.password = make_password("meliama95")
        user.my_set_password(raw_password=password)
        user.save()
        return user

    def create_superuser(self, email, password,username, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.my_set_password(raw_password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


# Profile Image
def get_profile_image_filepath(self):
    return f'profile_images/{self.pk}/{"profile_image.png"}'


def get_default_profile_image():
    return "empty.png"


class Customer(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    DOCUMENT_TYPE = (
        ("dni", "DNI"),
        ("cuit", "CUIT"),
        ("cuil", "CUIL"),
    )
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE)
    document_number = models.CharField(max_length=30)
    #email = models.EmailField(max_length=255, unique=True)
    email = models.CharField(max_length=30, unique=True)
    country_code = models.CharField(max_length=5)
    area_code = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=25)
    password = models.CharField(max_length=255)
    profile_image = models.ImageField(
        verbose_name="Foto de perfil",
        max_length=255,
        upload_to=get_profile_image_filepath,
        null=True,
        blank=True,
        default=get_default_profile_image,
    )
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "username",
        "last_name",
        "document_type",
        "document_number",
        "country_code",
        "area_code",
        "phone_number",
    ]

    objects = CustomerManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        #self.set_password(self.password)
        super().save(*args, **kwargs)
        # Check file type
        file_type = mimetypes.guess_type(self.profile_image.path)[0]
        if file_type not in ["image/jpeg", "image/png", "image/jpg"]:
            raise ValueError("La imagen debe ser jpg, jpg o png. ")
        try:
            image = Image.open(self.profile_image)
            width, height = image.size
            if image.verify():
                if width > 200 and height > 200:
                    image.thumbnail((200, 200))
                    image.save(self.profile_image.path)
            else:
                raise ValueError("No es una imagen válida.")

        except Exception as e:
            logging.error(e)
    
    def my_check_password(self, raw_password):
        print("Self.password: ", self.password)
        print("Raw password: ", raw_password)
        hashed_raw=make_password(raw_password)
        print("Hashed raw password: ", hashed_raw)
        result = self.password == hashed_raw
        print("my_check_password result", result)
        return result
    
    def my_set_password(self, raw_password):
        hashed=make_password(raw_password)
        self.password = hashed

