from django.test import TestCase, RequestFactory
from accounts.models import User
from booking.models import Booking, Location

class test_is_super_user(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.super = User.objects.create_superuser(customer_number="213456",email="obiwan@hellothere.com", password="greviouslovr98")
        self.user = User.objects.create_user(customer_number="984396",email="quigon@midiclorians.com", password="clorianboi123")
    
    def test_user(self):
        pass