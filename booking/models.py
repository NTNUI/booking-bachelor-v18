from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

#Location model
class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.name

#Booking model
class Booking(models.Model):
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    contact_date = models.DateField(_(u"Date"), blank=True)
    contact_time = models.TimeField(_(u"Time"), blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('booking_edit', kwargs={'pk': self.pk})




