from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from booking.filters import LocationFilter, UserFilter, AdminFilter
from django.contrib.auth.decorators import login_required
from .models import Booking, Location
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import BookingForm
from django.contrib import messages
from datetime import time
from calendar import Calendar
from groups.models import SportsGroup, Membership
from django.utils import timezone

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
def booking_all(request):
    book = []
    now = timezone.now()
    for booking in list(Booking.objects.filter()):
        book.append(booking)

    bookings = Booking.objects.all().filter(start__gte=now).order_by('start')
    booking_filter = AdminFilter(request.GET, queryset=bookings)
    return render(request, 'booking/booking_all.html', {
        'filter': booking_filter,
        'bookings': book
    })

def get_my_groups(request):
    user = request.user
    groups = Membership.objects.filter(person=user).values_list('group', flat=True)
    my_groups = []
    for g in groups:
        group = SportsGroup.objects.get(id=g).name
        my_groups.append(group)
    return my_groups

def confirmation_mail(request, pk):
    name = request.user.first_name
    booking = get_object_or_404(Booking, pk=pk)
    date = booking.get_date()
    (day, date, start_time, end_time) = date
    new_booking = 'Hey ' + name + ', you have created a new booking on ' + day + ', ' + date
    updated = 'Hey ' + name + ', your booking on ' + day + ', ' + date + ' has been updated!'
    deleted = 'Hey ' + name + ', your booking on ' + day + ', ' + date + ' has been deleted!'
    overwritten = 'Hey ' + name + ', your booking on ' + day + ', ' + date + ' has been overwritten!'
    queued = 'Hey ' + name + ', you have queued for a booking on ' + day + ', ' + date
    mails = (new_booking, updated, deleted, overwritten, queued)
    return mails

def booking_list(request):
    model = Booking
    bookings = model.objects.all()
    user = request.user
    now = timezone.now()
    my_bookings_list = get_my_bookings(request)
    my_groups = get_my_groups(request)
    my_group_bookings_list = []
    group_list = Booking.objects.none()
    for group in my_groups:
        booking = Booking.objects.filter(group=group).exclude(person=user).filter(start__gte=now).order_by('start')
        group_list = booking | group_list
        my_group_bookings_list.append(booking)

    return render(request, 'booking/bookings_list.html', {
        'my_bookings_list': my_bookings_list,
        'my_group_bookings_list': group_list,
        'bookings': bookings
    })

def get_my_bookings(request):
    model = Booking
    bookings = model.objects.all()
    user = request.user
    now = timezone.now()
    my_bookings_list = Booking.objects.filter(person=user).filter(start__gte=now).order_by('start')
    return my_bookings_list

def save_booking_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            my_bookings = get_my_bookings(request)

            data['html_booking_list'] = render_to_string('booking/includes/partial_booking_list.html', {
                'my_bookings_list': my_bookings
            })
            # messages.success(request, "Your booking request was successful")
            # confirmation_mail(request, )
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
        user = request.user
        form = BookingForm(user, request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            day = start.strftime("%A")
            date = start.strftime("%d %B")
            new_booking = 'Hey ' + user.first_name + ', you have created a new booking on ' + day + ', ' + date
            print(new_booking)
    else:
        user = request.user
        form = BookingForm(user, initial={'person': request.user})
    return save_booking_form(request, form, 'booking/includes/partial_booking_create.html')

def booking_create_from_calendar(request):
    if request.method == 'POST':
        user = request.user
        form = BookingForm(user, request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            day = start.strftime("%A")
            date = start.strftime("%d %B")
            new_booking = 'Hey ' + user.first_name + ', you have created a new booking on ' + day + ', ' + date
            print(new_booking)
    else:
        user = request.user
        form = BookingForm(user, initial={'person': request.user})
    return save_booking_form(request, form, 'booking/includes/partial_booking_create_calendar.html')


def booking_update(request, pk):
    mails = confirmation_mail(request, pk)
    book = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        user = request.user
        form = BookingForm(user, request.POST, instance=book)
        (new_booking, updated, deleted, overwritten, queued) = mails
        print(updated)
    else:
        user = request.user
        form = BookingForm(user, instance=book)
    return save_booking_form(request, form, 'booking/includes/partial_booking_update.html')

def booking_delete(request, pk):
    mails = confirmation_mail(request, pk)
    book = get_object_or_404(Booking, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        bookings = get_my_bookings(request)
        data['html_booking_list'] = render_to_string('booking/includes/partial_booking_list.html', {
            'my_bookings_list': bookings
        })
        (new_booking, updated, deleted, overwritten, queued) = mails
        print(deleted)
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('booking/includes/partial_booking_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

def show_form(request):
    return render(request, "booking/booking_form.html")
