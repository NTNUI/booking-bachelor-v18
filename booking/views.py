from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import Booking, Location, Request
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from booking.filters import AdminFilter
from django.template.loader import render_to_string
from .forms import BookingForm
from django.contrib.auth.decorators import user_passes_test
from .models import LOCATION_TYPES
from calendar import Calendar
from groups.models import SportsGroup, Membership
from django.utils import timezone
from django.shortcuts import render
import requests
import inspect


# Error page
def error_404(request):
    data = {}
    return render(request, 'booking/error_404.html', data)


# Render calendar page and returns lists of locations and types
@login_required
def index(request):
    model = Location
    locations = model.objects.all()
    type_list = LOCATION_TYPES
    return render(request, 'booking/booking.html', {
        'locations': locations,
        'types': type_list})


# Render 'My bookings' page and passes QuerySets relevant to that page.
@login_required
def booking_list(request):
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
    query = request.GET.get('q')
    if query:
        my_bookings_list = my_bookings_list.filter(
            Q(group__icontains=query) |
            Q(title__icontains=query)
        )
    return render(request, 'booking/bookings_list.html', {
        'my_bookings_list': my_bookings_list,
        'my_group_bookings_list': group_list,
    })


# Renders 'Manage bookings' page and passes QuerySets relevant to that page.
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='/')
def booking_manage(request):
    book = []
    now = timezone.now()
    for booking in list(Booking.objects.filter()):
        book.append(booking)

    bookings = Booking.objects.all().filter(start__gte=now).order_by('start')
    booking_filter = AdminFilter(request.GET, queryset=bookings)
    requested = Request.objects.filter(booking__id__in=booking_filter.qs)
    return render(request, 'booking/bookings_manage.html', {
        'filter': booking_filter,
        'bookings': book,
        'requested': requested,
    })


# API that allows client-side code to get data from database.
def api(request):
    model = Booking
    bookings = model.objects.all().values('title', 'description', 'start', 'end', 'location__name',
                                          'person__first_name', 'queueNo', 'group', 'person__id',
                                          'person__email', 'person__last_name')
    booking_list = list(bookings)
    return JsonResponse(booking_list, safe=False)


# Function used when creating, updating or deleting bookings.
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
            if form.cleaned_data['repeat'] == "weekly" and request.user.is_superuser:
                repeat_booking(form.cleaned_data)
            elif form.cleaned_data['repeat'] == "weekly":
                Request.objects.create(booking=form.instance, weekday=form.cleaned_data['day'].upper())
            # Sending create and queue mails
            if request.POST['repeat'] == 'weekly':
                name = request.user
                if request.user.is_superuser:
                    name = request.user
                    req_recurring = 'Hey ' + str(name) + ', you have created a recurring booking!'
                    send_mailgun_message(str(name.email), req_recurring)
                else:
                    req_recurring = 'Hey ' + str(name) + ', you have requested a recurring booking!'
                    send_mailgun_message(str(name.email), req_recurring)
            elif inspect.stack()[1][3] != 'booking_update':
                booking = Booking.objects.all().last()
                name = request.user
                if booking.queueNo == 0:
                    created = 'Hey ' + str(name) + ', you have created a new booking!'
                    send_mailgun_message(str(name.email), created)
                else:
                    queued = 'Hey ' + str(name) + ', you have queued for a booking!'
                    send_mailgun_message(str(name.email), queued)
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


# Function used to create new bookings
def booking_create(request):
    if request.method == 'POST':
        user = request.user
        form = BookingForm(user, request.POST)

    else:
        user = request.user
        form = BookingForm(user, initial={'person': request.user})
    return save_booking_form(request, form, 'booking/includes/partial_booking_create.html')


# Function used to create new booking from the calendar interface
def booking_create_from_calendar(request):
    if request.method == 'POST':
        user = request.user
        form = BookingForm(user, request.POST)
    else:
        user = request.user
        form = BookingForm(user, initial={'person': request.user})
    return save_booking_form(request, form, 'booking/includes/partial_booking_create_calendar.html')


# Function used to edit/update bookings
def booking_update(request, pk):
    book = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        user = request.user
        form = BookingForm(user, request.POST, instance=book)
        # Sending update mails
        update = 'Hey ' + str(user) + ', you have updated a booking!'
        send_mailgun_message(str(user.email), update)
        if str(user) != str(book.person):
            overwritten = 'Hey ' + str(book.person) + ', your booking has been overwritten!'
            send_mailgun_message(str(book.person.email), overwritten)
    else:
        user = request.user
        form = BookingForm(user, instance=book)
    return save_booking_form(request, form, 'booking/includes/partial_booking_update.html')


# Function used to delete bookings
def booking_delete(request, pk):
    book = get_object_or_404(Booking, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        user = request.user
        data['form_is_valid'] = True  # This is just to play along with the existing code
        bookings = get_my_bookings(request)
        data['html_booking_list'] = render_to_string('booking/includes/partial_booking_list.html', {
            'my_bookings_list': bookings
        })
        # Sending delete mails
        delete = 'Hey ' + str(user) + ', a booking has been deleted!'
        send_mailgun_message(str(user.email), delete)
        if str(user) != str(book.person):
            overwritten = 'Hey ' + str(book.person) + ', your booking has been overwritten!'
            send_mailgun_message(str(book.person.email), overwritten)
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('booking/includes/partial_booking_delete.html', context, request=request, )
    return JsonResponse(data)


# Function used to create recurring bookings.
def repeat_booking(data):
    location = data['location']
    start = data['start']
    end = data['end']
    if data['repeat'] == "noRepeat":
        repeat = False
    elif data['repeat'] == "weekly":
        repeat = True
    else:
        repeat = False
    
    day_map = {"MON" : 0, "TUE":1, "WED":2, "THU" : 3, 
        "FRI":4, "SAT":5, "SUN":6
    }
    dayofweek = day_map[data['day'].upper()]
    year = int(start.year)
    month = int(start.month)
    day = int(start.day)
    loc = location
    s_time = str(start)[11:] #get time substring
    e_time = str(end)[11:] #YYYY-MM-DDTHH:MMZ
    title = data['title']
    descr = data['description']
    person = data['person']
    group = data['group']
    cal = Calendar()
    ydcal = cal.yeardays2calendar(year, width=6)
    if month > 5:
        w = ydcal[1]
    else:
        w = ydcal[0]
    for m in range(len(w)):
        if m+1 < month:
            continue  # skip past months
        for k in range(len(w[m])):
            for d in range(len(w[m][k])):
                cal_day = w[m][k][d]
                if (cal_day[0] <= day and m+1 == month) or cal_day[0]==0:
                    continue
                if cal_day[1] == dayofweek:
                    if m < 9:  # format month
                        cal_m = "0" + str(m+1)
                    else:
                        cal_m = str(m+1)
                    if cal_day[0] < 9:  # format day
                        cal_d = "0" + str(cal_day[0])
                    else:
                        cal_d = str(cal_day[0])
                        
                    date_format = str(year) + "-" + cal_m + "-" + cal_d
                    start_rec = date_format + " " + s_time
                    end_rec = date_format + " " + e_time
                    booking = Booking(location=location, start=start_rec, group=group, end=end_rec, title=title,
                                      description=descr, person=person)
                    booking.save(repeatable=True)
    for data_elements in data:
        if data_elements == "request":
            data["request"].delete()


# Function used to accept recurring booking requests
def accept_request(request, pk):
    if request.method == 'POST':
        req = get_object_or_404(Request, pk=pk)
        data = {
            'location': req.booking.location,
            'person': req.booking.person,
            'start': req.booking.start,
            'end': req.booking.end,
            'group': req.booking.group,
            'title': req.booking.title,
            'description': req.booking.description,
            'day': req.weekday,
            'repeat': "weekly",
            'request': req,
        }
        # Sending accepted mails
        accept = 'Hey ' + str(request.user) + ', you have accepted a recurring booking!'
        send_mailgun_message(str(request.user.email), accept)
        req_accept = 'Hey ' + str(req.booking.person) + ', your recurring booking has been accepted!'
        send_mailgun_message(str(req.booking.person.email), req_accept)

        repeat_booking(data)
        return HttpResponseRedirect('/booking/bookings_manage')


# Function used to accept recurring booking requests
def decline_request(request, pk):
    if request.method == 'POST':
        req = get_object_or_404(Request, pk=pk)
        req.delete()
        # Sending declined mails
        decline = 'Hey ' + str(request.user) + ', you have declined a recurring booking!'
        send_mailgun_message(str(request.user.email), decline)
        req_decline = 'Hey ' + str(req.booking.person) + ', your recurring booking has been declined!'
        send_mailgun_message(str(req.booking.person.email), req_decline)
        return HttpResponseRedirect('/booking/bookings_manage')


# Get groups of logged-in user
def get_my_groups(request):
    user = request.user
    groups = Membership.objects.filter(person=user).values_list('group', flat=True)
    my_groups = []
    for g in groups:
        group = SportsGroup.objects.get(id=g).name
        my_groups.append(group)
    return my_groups


# Returns a list of bookings made by the logged-in user.
def get_my_bookings(request):
    user = request.user
    now = timezone.now()
    my_bookings_list = Booking.objects.filter(person=user).filter(start__gte=now).order_by('start')
    return my_bookings_list


# Function used when sending emails through Mailgun
def send_mailgun_message(user, text):
    return requests.post(
        'https://api.mailgun.net/v3/mg.ntnui.no/messages',
        auth=("api", 'key-f90e4c24dcfdb08ea58481344645d540'),
        data={"from": "support@ntnui.no",
              "to": [user],
              "subject": 'NTNUI - Booking update',
              "html": text + " Go to http://127.0.0.1:8000/booking/bookings_list/ to see the changes!"})
