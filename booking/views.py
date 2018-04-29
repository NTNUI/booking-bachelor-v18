from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from booking.filters import AdminFilter
from .models import Booking, Location
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import BookingForm
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages
from datetime import time
from groups.models import SportsGroup
from groups.models import Membership
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

def locationApi(request, **kwargs):
    model = Location
    locations = model.objects.all().values('name', 'address', 'description', 'type')
    location_list = list(locations)
    return JsonResponse(location_list, safe=False)

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

