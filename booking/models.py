from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

#Booking model
class Booking(models.Model):
    person = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    contact_date = models.DateField(_(u"Date"), blank=True)
    contact_time = models.TimeField(_(u"Time"), blank=True)


    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('booking_edit', kwargs={'pk': self.pk})

