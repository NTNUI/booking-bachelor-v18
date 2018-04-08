from datetime import date, datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from groups.models import SportsGroup
from groups.models import Membership
from django.contrib.auth.models import User
from django.db.utils import OperationalError

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

    try:
        tu = tuple(SportsGroup.objects.all().values_list('name', 'name'))
        if not tu:
            tu = (
                ('', '---------'),
            )
        else:
            tu = tuple(SportsGroup.objects.all().values_list('name', 'name'))

    except OperationalError:
        tu = (
            ('', '---------'),
        )

    group = models.CharField(max_length=200, choices=tu, blank=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('booking_edit', kwargs={'pk': self.pk})

    def get_group(self):
        thelist = Membership.objects.filter(person=self.person).values('group')
        print(thelist)
        my_groups = []
        for x in thelist:
            my_groups.append(x)
        return my_groups
