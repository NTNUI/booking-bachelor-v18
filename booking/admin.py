from django.contrib import admin
from .models import Booking, Location, Request

# Register your models here.

admin.site.register(Booking)
admin.site.register(Location)
admin.site.register(Request)

