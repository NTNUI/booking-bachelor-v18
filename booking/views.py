from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Booking



@login_required
def index(request):
    return render(request, 'booking/booking.html')

class BookingList(ListView):
    model = Booking

class BookingCreate(CreateView):
    model = Booking
    success_url = reverse_lazy('booking')
    fields = ['person', 'name', 'location', 'contact_date', 'contact_time', 'description']
    def get_initial(self):
        return {'person': self.request.user}

class BookingUpdate(UpdateView):
    model = Booking
    success_url = reverse_lazy('booking_list')
    fields = ['name', 'location', 'contact_date', 'contact_time', 'description']

class BookingDelete(DeleteView):
    model = Booking
    success_url = reverse_lazy('booking_list')

class NewsCreateView(CreateView):
    model = Booking
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, reverse_lazy('booking_list'), {'news': self.object})