from datetime import date, datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

LOCATION_TYPES = (
    ('gym ','GYM'),
    ('football field', 'FOOTBALL FIELD'),
    ('volleyball grounds','VOLLEYBALL GROUNDS')
)

#Location model
class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    type = models.CharField(max_length=200, choices=LOCATION_TYPES, default='gym')

    def __str__(self):
        return self.name

#Booking model
class Booking(models.Model):
    person = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=400, default='')
    description = models.CharField(max_length=400, default='')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    start = models.DateTimeField(_(u'Start'), blank=True)
    end = models.DateTimeField(_(u'End'), blank=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('booking_edit', kwargs={'pk': self.pk})

