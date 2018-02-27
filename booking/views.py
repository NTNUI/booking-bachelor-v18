from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from requests import request

from accounts.models import User
from booking.filters import LocationFilter, UserFilter
from .models import Booking, Location


@login_required
def index(request):
    return render(request, 'booking/booking.html')

class BookingList(ListView):
    model = Booking

    def all(request):
        locations = []
        bookings = []
        for location in list(Location.objects.filter()):
            locations.append(location.name)
        for booking in list(Booking.objects.filter()):
            bookings.append(booking)
        return render(request, 'booking/booking_list.html', {
            'locations': locations,
            'bookings': bookings, })

@login_required
def BookingAll(request):
        locations = []
        bookings = []
        location_list = Booking.objects.all()
        location_filter = LocationFilter(request.GET, queryset=location_list)
        for location in list(Location.objects.filter()):
            locations.append(location.name)
        for booking in list(Booking.objects.filter()):
            bookings.append(booking)
        return render(request, 'booking/booking_all.html', {
            'locations': locations,
            'bookings': bookings,
            'filter': location_filter, })

class BookingCreate(CreateView):
    model = Booking
    success_url = reverse_lazy('booking')
    fields = ['person', 'location', 'start', 'end', 'description']
    def get_initial(self):
        return {'person': self.request.user}

class BookingUpdate(UpdateView):
    model = Booking
    success_url = reverse_lazy('booking_list')
    fields = ['location', 'start', 'end', 'description']

class BookingDelete(DeleteView):
    model = Booking
    success_url = reverse_lazy('booking_list')

class NewsCreateView(CreateView):
    model = Booking
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, reverse_lazy('booking_list'), {'news': self.object})
