from datetime import date, datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

#Location model
class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.name

#Booking model
class Booking(models.Model):
    person = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    contact_date = models.DateField(_(u'Date'), blank=True, default=date.today().strftime('%m/%d/%Y'))
    contact_time = models.TimeField(_(u'Time'), blank=True, default=datetime.now())
    description = models.CharField(max_length=400, default='')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('booking_edit', kwargs={'pk': self.pk})




