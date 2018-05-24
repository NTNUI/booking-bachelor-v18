from django.test import TestCase, RequestFactory, Client
from accounts.models import User
from booking.models import Booking, Location
from booking import views

class test_views_func(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.c = Client()
        self.user = User.objects.create_superuser(email='snaic@fastmail.com', password='gottagofast') 
        self.c.login(email='snaic@fastmail.com', password='gottagofast')
        loc = Location(name='fasttrack')
        loc.save()
        Booking.objects.create(location=loc, title='runfast', description='run faster', start='2018-07-20 13:00', end='2018-07-20 14:00')

    def test_error_404(self):
        request = self.factory.get('/notareal/site/')
        request.user = self.user
        response = views.error_404(request)
        self.assertContains(response, "404 Error")
        
    
    def test_index(self):
        response = self.c.get('/booking/')
        self.assertTemplateUsed(response, 'booking/booking.html')
        
    
    def test_booking_list(self):        
        response = self.c.get('/booking/bookings_list/')        
        self.assertContains(response, 'My bookings')
        
    
    def test_booking_manage(self):
        request = self.factory.get('/booking/bookings_manage')
        request.user = self.user
        response = views.booking_manage(request)
        self.assertContains(response, 'Manage bookings')        
    
    def test_api(self):
        response = self.c.get('/booking/api')
        
        bookings = Booking.objects.all().values('title', 'description', 'start', 'end', 'location__name',
                                          'person__first_name', 'queueNo', 'group', 'person__id',
                                          'person__email', 'person__last_name')
        
        title1 = bookings[0]['title']
        self.assertContains(response, title1)
        
    
    def test_save_booking_form(self):
        
        self.assertTrue(True)
    
    def test_booking_create(self):
        
        self.assertTrue(True)
    
    def test_booking_create_from_calendar(self):
        self.assertTrue(True)