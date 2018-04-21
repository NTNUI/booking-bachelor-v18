from django import forms
from .models import Booking
from groups.models import SportsGroup
from groups.models import Membership

#Form used for creating, editing and deleting bookings.
class BookingForm(forms.ModelForm):
    # Add user groups to form
    def __init__(self, user, *args, **kwargs):
        blank_choice = (('', '---------'),)
        super(BookingForm, self).__init__(*args, **kwargs)
        member_objects = Membership.objects.filter(person=user).values_list('group', flat=True)
        my_groups = []
        for choices, choice_id in enumerate(member_objects):
            sport_objects = SportsGroup.objects.get(id=str(choice_id)).name
            my_groups.append((sport_objects, sport_objects))
        choices = tuple(my_groups)
        self.fields['group'] = forms.ChoiceField(
            choices=blank_choice + choices, required=False)

    class Meta:
        model = Booking
        fields = ['person', 'location', 'start', 'end', 'title', 'description', 'group']
        # Hide person field because it will be automatically added.
        widgets = {'person': forms.HiddenInput()}