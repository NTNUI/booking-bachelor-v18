from django.contrib import admin
from .models import Booking

# Register your models here.

# Register booking model to admin site.
admin.site.register(Booking)