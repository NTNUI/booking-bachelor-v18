from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from booking.filters import LocationFilter, UserFilter
from .models import Booking, Location
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import BookingForm
from django.contrib import messages
from datetime import time


@login_required
def index(request):
    model = Location
    locations = model.objects.all()
    return render(request, 'booking/booking.html', {
        'locations': locations})


def api(request, **kwargs):
    model = Booking
    bookings = model.objects.all().values('title', 'description', 'start', 'end', 'location__name', 'person__first_name', 'queueNo')
    booking_list = list(bookings)
    return JsonResponse(booking_list, safe=False)

def api2(request, **kwargs):
    #DEPRECATED
    b = Booking.objects.all()#.values('title', 'description', 'start', 'end', 'location__name'     )
    hours = Booking.objects.raw('SELECT id, start, end FROM booking_Booking WHERE queueNo = 0')
    b2 = Booking.objects.raw('SELECT id, start, end FROM booking_Booking WHERE SUBSTR(start, 1, 10) = "2018-05-05"')
    print("HELLO")
    dates = {}
    for b in hours:
        date = b.start
        d = b.end-b.start
        date_key = str(date.year)+str(date.month)+str(date.month)
        if date_key in dates.keys():
            dates[date_key]+= d
        else:
            dates[date_key]=d
    #convert to rounded integer
    for k in dates.keys():
        s = dates[k].total_seconds()
        h = s//3600
        m = (s-h)//60
        if m > 30:
            dates[k] = h
        else:
            dates[k] = h+1
    b2_list = list(b2)
    hours_list = [(i, j) for i, j in zip(dates.keys(), dates.values())]
    return JsonResponse(hours_list+b2_list, safe=False)

class BookingList(ListView):
    model = Booking

    def all(self, request):
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

def booking_list(request):
    model = Booking
    bookings = model.objects.all()
    return render(request, 'booking/bookings_list.html', {
        'bookings': bookings})

def confirmation_mail(request):
    name = request.user.first_name
    body = "Hey " + name + ", you have created a new booking!"
    print(body)

def save_booking_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            bookings = Booking.objects.all()
            data['html_booking_list'] = render_to_string('booking/includes/partial_booking_list.html', {
                'bookings': bookings
            })
            # messages.success(request, "Your booking request was successful")
            confirmation_mail(request)
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def booking_create(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
    else:
        form = BookingForm(initial={'person': request.user})
    return save_booking_form(request, form, 'booking/includes/partial_booking_create.html')

def booking_create_from_calendar(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
    else:
        form = BookingForm(initial={'person': request.user})
    return save_booking_form(request, form, 'booking/includes/partial_booking_create_calendar.html')


def booking_update(request, pk):
    book = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=book)
    else:
        form = BookingForm(instance=book)
    return save_booking_form(request, form, 'booking/includes/partial_booking_update.html')

def booking_delete(request, pk):
    book = get_object_or_404(Booking, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        bookings = Booking.objects.all()
        data['html_booking_list'] = render_to_string('booking/includes/partial_booking_list.html', {
            'bookings': bookings
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('booking/includes/partial_booking_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)