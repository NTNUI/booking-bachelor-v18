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


@login_required
def index(request):
    return render(request, 'booking/booking.html')

def api(request, **kwargs):
    model = Booking
    bookings = model.objects.all().values('description', 'start', 'end', 'location__name', 'person__first_name')
    hours = Booking.objects.raw('SELECT SUM(end - start) AS s, start, queueNo FROM Booking WHERE queueNo = 0 GROUP BY SUBSTRING(start, 1, 10) HAVING s>0')
    hours_list = list(hours)

    booking_list = list(bookings)
    return JsonResponse(booking_list+hours_list, safe=False)

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
    template_name = "booking/booking_confirm_edit.html"
    success_url = reverse_lazy('booking_list')
    fields = ['location', 'end', 'description']

class BookingDelete(DeleteView):
    model = Booking
    success_url = reverse_lazy('booking_list')


def booking_list(request):
    model = Booking
    bookings = model.objects.all()
    return render(request, 'booking/bookings_list.html', {
        'bookings': bookings})

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