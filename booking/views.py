from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from booking.filters import UserFilter, AdminFilter#, LocationFilter,
from django.contrib.auth.decorators import login_required
from .models import Booking, Location
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from .forms import BookingForm
from django.contrib.auth.decorators import user_passes_test

from .models import LOCATION_TYPES
from django.contrib import messages #TODO: check if actually used
from datetime import time
from calendar import Calendar
from groups.models import SportsGroup, Membership
from django.utils import timezone

@login_required
def index(request):
    model = Location
    locations = model.objects.all()
    type_list = LOCATION_TYPES
    return render(request, 'booking/booking.html', {
        'locations': locations,
        'types': type_list})


def api(request, **kwargs):
    model = Booking
    bookings = model.objects.all().values('title', 'description', 'start', 'end', 'location__name', 'person__first_name', 'queueNo', 'group')
    booking_list = list(bookings)
    return JsonResponse(booking_list, safe=False)

def api2(request, **kwargs):
    #DEPRECATED
    pass


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


def repeatBooking(form):
    location = form.cleaned_data['location']
    start = form.cleaned_data['start']
    end = form.cleaned_data['end']
    if form.cleaned_data['repeat'] == "noRepeat":
        repeat = False
    elif form.cleaned_data['repeat'] == "weekly":
        repeat = True
    else:
        repeat = False
    
    day_map = {"MON" : 0, "TUE":1, "WED":2, "THU" : 3, 
        "FRI":4, "SAT":5, "SUN":6
    }
    dayofweek = day_map[form.cleaned_data['day'].upper()]
    year = int(start.year)
    month = int(start.month)
    day = int(start.day)
    loc = location
    s_time = str(start)[11:]#.replace("+", ":") #get time substring
    e_time = str(end)[11:]#.replace("+", ":") #YYYY-MM-DDTHH:MMZ
    title = form.cleaned_data['title']
    descr = form.cleaned_data['description']
    person = form.cleaned_data['person'] 
    cal = Calendar()
    ydcal = cal.yeardays2calendar(year, width=6)
    if month > 5:
        w = ydcal[1]
    else:
        w = ydcal[0]
    for m in range(len(w)):
        if m+1 < month:
            continue #skip past months 
        for k in range(len(w[m])):
            for d in range(len(w[m][k])):
                cal_day = w[m][k][d]
                if (cal_day[0] <= day and m+1 == month) or cal_day[0]==0:
                    continue
                if cal_day[1]==dayofweek:
                    if m <9: #format month
                        cal_m = "0"+str(m+1)
                    else:
                        cal_m = str(m+1)
                    if cal_day[0]<9: #format day
                        cal_d = "0"+str(cal_day[0])
                    else:
                        cal_d = str(cal_day[0])
                    date_format = str(year)+"-"+cal_m+"-"+cal_d 
                    start_rec = date_format+" "+s_time
                    end_rec = date_format+" "+e_time
                    b = Booking(location=loc, start=start_rec, end=end_rec, title=title, description=descr, person=person)
                    b.save(repeatable=True)



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
            if form.cleaned_data['repeat'] == "weekly":
                repeatBooking(form)
            # messages.success(request, "Your booking request was successful")
            # confirmation_mail(request, )
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
        print(form)
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
