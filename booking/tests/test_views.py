from django.test import TestCase, RequestFactory
from accounts.models import User
from booking.models import Booking, Location

class test_views_func(TestCase):

    def setUp(self):
        pass

    def test_error_404(self):
        self.assertTrue(True)
    
    def test_index(self):
        self.assertTrue(True)
    
    def test_booking_list(self):
        self.assertTrue(True)
    
    def test_booking_manage(self):
        self.assertTrue(True)
    
    def test_api(self):
        self.assertTrue(True)
    
    def test_save_booking_form(self):
        self.assertTrue(True)
    
    def test_booking_create(self):
        self.assertTrue(True)
    
    def test_booking_create_from_calendar(self):
        self.assertTrue(True)