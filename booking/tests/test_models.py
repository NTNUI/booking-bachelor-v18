from django.test import TestCase, Client
from accounts.models import User
from booking.models import Booking, Location

class test_location(TestCase):

    def setUp(self):
        self.location = Location.objects.create(name="sand", address="Tatooine st. 12", description="its coarse rough and gets everywhere")
    
    def test_name(self):
        self.assertTrue(str(self.location) == "sand")


class test_booking(TestCase):

    def setUp(self):
        self.loc = Location.objects.create(name="BroGym", address="Brophessor st. 12", description="best gym get swole 100\%\ gains guaranteed live large die large leave a huge coffin")
        self.user = User.objects.create_superuser(customer_number="92837465",email="arnold@steroids.com", password="steroidboi123")
        self.b1 = Booking(id=1, person=self.user, title="Baiceps", description="get de big baiceps", location=self.loc, start="2019-05-15T12:00:00Z", end="2019-05-15T14:00:00Z")
        self.b1.save()
        self.b2 = Booking(id=2, person=self.user, title="legs", description="skip legday", location=self.loc, start="2019-05-15T12:00:00Z", end="2019-05-15T14:00:00Z")
        self.b2.save()
    
    def test_name(self):
        self.assertTrue(str(self.b1) == "Baiceps")
    
    def test_absolute_url(self):
        pass

    def test_move_queue(self):
        before1 = self.b1.queueNo
        before2 = self.b2.queueNo
        queue = [self.b1, self.b2]
        self.b1.move_queue(queue, 1)
        self.assertGreater(self.b1.queueNo, before1)
        self.assertGreater(self.b2.queueNo, before2)
    
    def test_save(self):
        before = self.b2.queueNo
        self.b2.save({
            'id': 2,
            'start':'2019-05-15T14:00', 
            'end':'2019-05-15T16:00'})
        self.assertGreater(before, self.b2.queueNo)
    
    def test_delete(self):
        before = self.b2.queueNo
        self.b1.delete()
        q1 = Booking.objects.all()[0]
        self.assertGreater(before, q1.queueNo)
    
    def test_get_groups(self):
        groups = self.b1.get_groups()
        self.assertEqual([], groups)
    
    def test_get_date(self):
        dates = self.b1.get_date()
        self.assertEqual(dates[0], "Wednesday")
        self.assertEqual(dates[1], "15 May")
        self.assertEqual(dates[2], "12:00")
        self.assertEqual(dates[3], "14:00")
        