from django.contrib.auth.models import User
import django_filters
from django.db.models import TextField

import accounts
from booking.models import Location, Booking


class AdminFilter(django_filters.FilterSet):
    title = django_filters.CharFilter()
    person = django_filters.ModelChoiceFilter(queryset=accounts.models.User.objects.all())
    class Meta:
        model = Booking
        fields = ['location', 'person', 'title', 'start', 'group']

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {'first_name'}