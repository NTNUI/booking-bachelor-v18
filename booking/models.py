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
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    start = models.DateTimeField(_(u'Start'), blank=True)
    end = models.DateTimeField(_(u'End'), blank=True)
    description = models.CharField(max_length=400, default='')
    queueNo = models.IntegerField(default=0)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('booking_edit', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        print(self.start)
        print(self.location)
        model = Booking
        bookings = model.objects.filter(location=self.location, start=self.start, end=self.end)
        # bookings = list(bookings)
        if list(bookings) != []:
            # self.queueNo = max(bookings, (item.queueNo for item in bookings))
            maxVal =  bookings.aggregate(models.Max('queueNo'))
            temp = [maxVal [i] for i in sorted(maxVal.keys())]
            self.queueNo = int(temp[0])+1
            # self.queueNo += 1
            print(self.queueNo)
        print(bookings)
        return super(Booking, self).save(*args, **kwargs)