from django import forms
from .models import Booking

#Form used for creating, editing and deleting bookings.
class BookingForm(forms.ModelForm):
    
    def save(repeatable=False, *args, **kwargs):

        return super()
    class Meta:
        model = Booking
        fields = ['person', 'location', 'start', 'end', 'title', 'description', 'group']
        # Hide person field because it will be automatically added.
        widgets = {'person': forms.HiddenInput()}
        
    repeating = forms.BooleanField(required=False)
        