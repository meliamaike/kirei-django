from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from PIL.Image import Image
import logging
import mimetypes

class CustomerManager(BaseUserManager):
    #customer = user
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Debe ingresar un email.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password) #hashing password
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


#Profile Image
def get_profile_image_filepath(self):
    return f'profile_images/{self.pk}/{"profile_image.png"}'

def get_default_profile_image():
    return "empty.png"

class Customer(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    DOCUMENT_TYPE = (
    ('dni', 'DNI'),
    ('cuit', 'CUIT'),
    ('cuil', 'CUIL'),
)
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE)
    document_number = models.CharField(max_length=30)
    email = models.EmailField(max_length=255, unique=True)
    country_code = models.CharField(max_length=5)
    area_code = models.CharField(max_length=5)
    phone_number = PhoneNumberField()
    password = models.CharField(max_length=255)
    profile_image = models.ImageField(
        verbose_name="Foto de perfil",
        max_length=255,
        upload_to=get_profile_image_filepath,
        null=True,
        blank=True,
        default=get_default_profile_image,
    )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'document_type', 'document_number', 'country_code', 'area_code', 'phone_number']

    objects = CustomerManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)
        # Check file type
        file_type = mimetypes.guess_type(self.profile_image.path)[0]
        if file_type not in ['image/jpeg', 'image/png', 'image/jpg']:
            raise ValueError("La imagen debe ser jpg, jpg o png. ")
        try:
            image = Image.open(self.profile_image)
            width, height = image.size
            if image.verify():
                if width > 200 and height > 200:
                    image.thumbnail((200,200))
                    image.save(self.profile_image.path)
            else:
                raise ValueError('No es una imagen válida.')

        except Exception as e:
            logging.error(e)
        

    def set_password(self, password):
        validate_password(password)
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)


