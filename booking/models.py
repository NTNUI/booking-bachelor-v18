from django.db import models

# Create your models here.

class Booking(models.Model):
    date_issued = models.DateField(auto_now_add=True)
    booking_id = models.AutoField(primary_key=True)
    customer_number = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
    )
    location_id = models.ForeignKey(
        'Location',
        on_delete=models.CASCADE,
    )

class Location(models.Model):
    location_id = models.ForeignKey(
        'Location',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=12)
    description = models.TextField(max_length=200)

