from django import forms
from .models import Booking

#Form used for creating, editing and deleting bookings.
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['person', 'location', 'start', 'end', 'title', 'description', 'group']
        # Hide person field because it will be automatically added.
        widgets = {'person': forms.HiddenInput()}