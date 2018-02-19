from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from booking.models import Booking
from django.http import HttpResponse
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy


# Create your views here.


@login_required
def index(request):

    return render(request, 'booking/booking.html')


class BookingList(ListView):
    model = Booking

class BookingCreate(CreateView):
    model = Booking
    success_url = reverse_lazy('booking_list')
    fields = ['name', 'location', 'contact_date', 'contact_time']

class BookingUpdate(UpdateView):
    model = Booking
    success_url = reverse_lazy('booking_list')
    fields = ['name', 'location', 'contact_date', 'contact_time']

class BookingDelete(DeleteView):
    model = Booking
    success_url = reverse_lazy('booking_list')