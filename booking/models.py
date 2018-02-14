from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import datetime

# Create your models here.

class Booking(models.Model):
    date_issued = models.DateField(auto_now_add=True)
    booking_id = models.AutoField(primary_key=True)
    customer_number = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
    )
    location_id = models.ForeignKey(
        'Location',
        on_delete=models.CASCADE,
    )

class Location(models.Model):
    booking_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=12)
    description = models.TextField(max_length=200)






