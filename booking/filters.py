from django.contrib.auth.models import User
import django_filters

from booking.models import Location, Booking


class LocationFilter(django_filters.FilterSet):
    class Meta:
        model = Booking
        fields = ['location']

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {'first_name'}