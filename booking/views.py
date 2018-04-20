from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from booking.filters import LocationFilter, UserFilter
from .models import Booking, Location
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import BookingForm
from django.contrib import messages
from datetime import time
from calendar import Calendar


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
    pass


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
@user_passes_test(lambda u: u.is_superuser)
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
            #TODO:replace request.repeat with actual name
            #get dayNr from request
            #request.repeat
            repeat = False
            #TODO: replace with actual data from form 
            dayofweek = 0
            year = 2018
            loc = "location"
            s_time = "12:00"
            e_time = "14:00"
            title = "TITLE"
            descr = "description"
            #TODO: skip past dates
            if repeat:
                cal = Calendar()
                ydcal = cal.yeardays2calendar(year, width=6)
                for w in ydcal:
                    for month in w:
                        for week in month:
                            for day in week:
                                if day[1]==dayofweek:
                                    month_nr = w.index(month)+ydcal.index(w)+1
                                    date_format = str(year)+"-"+str(month_nr)+"-"+str(day[0])
                                    start = date_format+" "+s_time
                                    end = date_format+" "+e_time
                                    b = Booking(location=loc, start=start, end=end, title=title, description=descr)
                                    b.save(repeatable=True)


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

def show_form(request):
    return render(request, "booking/booking_form.html")