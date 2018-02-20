from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django import *
from django.conf import settings
from django.contrib.auth import get_user_model
from booking.models import Booking
from django.http import HttpResponse
from django.views.generic import TemplateView,ListView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from accounts.models import User
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Booking
from .forms import BookingForm

@login_required
def index(request):
    return render(request, 'booking/booking.html')

class BookingList(ListView):
    model = Booking

class BookingCreate(CreateView):
    model = Booking
    success_url = reverse_lazy('booking_list')
    fields = ['person', 'name', 'location', 'contact_date', 'contact_time']
    def get_initial(self):
        return {'person': self.request.user}

class BookingUpdate(UpdateView):
    model = Booking
    success_url = reverse_lazy('booking_list')
    fields = ['name', 'location', 'contact_date', 'contact_time']

class BookingDelete(DeleteView):
    model = Booking
    success_url = reverse_lazy('booking_list')

# at the top of the file

def booking_create(request):
    booking_form = BookingForm()
    return render(request, "bookingform.html", {"form": booking_form})