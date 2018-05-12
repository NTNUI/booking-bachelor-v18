from django.db import models
from django_filters import CharFilter, FilterSet, ModelChoiceFilter
from accounts.models import User
from booking.models import Booking


class AdminFilter(FilterSet):
    person = ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Booking
        fields = ['location', 'person', 'title', 'start', 'group']
        filter_overrides = {
            models.CharField: {
                'filter_class': CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }