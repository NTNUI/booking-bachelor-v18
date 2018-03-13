from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, render_to_response, HttpResponseRedirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Booking
from django.http import JsonResponse, request
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User
from booking.filters import LocationFilter, UserFilter
from .models import Booking, Location
from booking.decorators import is_super_user


@login_required
def index(request):
    return render(request, 'booking/booking.html')

def api(request, **kwargs):
    model = Booking
    bookings = model.objects.all().values('description', 'start', 'end', 'location__name', 'person__first_name')
    booking_list = list(bookings)
    return JsonResponse(booking_list, safe=False)

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

@is_super_user
def restr_site(request):
    return HttpResponse("<h1>FYFY!!!</h1>")