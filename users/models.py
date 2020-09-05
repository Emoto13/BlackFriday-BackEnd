# Create your models here.


from django.contrib.auth.base_user import AbstractBaseUser 
from django.contrib.auth.models import UserManager
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField

# Create your models here.

# username
# first_name
# last_name
# email
# password
# groups
# user_permissions
# is_staff
# is_active
# is_superuser
# last_login
# date_joined

GENDERS = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
    ('Prefer not to specify', 'Prefer not to specify')
]


class CustomUser(AbstractBaseUser):
    USERNAME_FIELD = 'username'

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    description = models.TextField(default='')
    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150)

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_logged_in = models.BooleanField(default=True)
    last_login = models.DateTimeField(default=timezone.now)
    date_joined = models.DateField(auto_now_add=True)

    profile_image = models.ImageField(blank=True, null=True)

    birthday = models.DateField(blank=True, null=True)
    account_title = models.CharField(blank=True, default='', max_length=50, null=True)

    latitude = models.DecimalField(
        max_digits=50, decimal_places=30, blank=True, null=True)
    longitude = models.DecimalField(
        max_digits=50, decimal_places=30, blank=True, null=True)

    gender = models.CharField(choices=GENDERS, max_length=50)
    apartment = models.CharField(max_length=10)
    floor = models.CharField(max_length=10)
    street_and_number = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    country = CountryField(blank=True)
    zip = models.IntegerField(null=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.id} - {self.username} {self.first_name} {self.last_name}"