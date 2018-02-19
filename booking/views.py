from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django import *
from django.conf import settings
from django.contrib.auth import get_user_model

from booking.models import Booking
from django.http import HttpResponse
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from accounts.models import User
from django.contrib.auth.models import User


# Create your views here.
from ntnui.decorators import is_member


@login_required
def index(request):
    return render(request, 'booking/booking.html')

class BookingList(ListView):
    model = Booking

class BookingCreate(CreateView):
    model = Booking
    #user = accounts.User.first_name
    #print(user)
    success_url = reverse_lazy('booking_list')
    fields = ['person', 'name', 'location', 'contact_date', 'contact_time', 'description']
    def get_initial(self):

        return {"name": ""}

class BookingUpdate(UpdateView):
    model = Booking
    success_url = reverse_lazy('booking_list')
    fields = ['name', 'location', 'contact_date', 'contact_time', 'description']

class BookingDelete(DeleteView):
    model = Booking
    success_url = reverse_lazy('booking_list')