from django.test import TestCase, Client
from accounts.models import User
from booking.models import Booking, Location

class test_enqueue(TestCase):

    def setUp(self):
        mail = "test@example.com"
        pswrd = "TestyTest123"
        User.objects.create_superuser(email=mail, password=pswrd)
        self.login_response = self.client.login(email=mail, password=pswrd)
        Location.objects.create(name="Idrettshallen")

    def test_g(self):
        self.assertGreater(2, 1)

    def test_enqueued(self):
        loc = "Idrettshallen"
        start = "2018-04-15 10:00:00"
        end = "2018-04-15 13:00:00"
        location = Location.objects.get(name=loc)
        response = self.client.post("/booking_list/create", {"location": location,
                                                "Start": start,
                                                "End": end,
                                                "Description": "Dollyball"})
        self.client.post("/booking_list/create", {"location": location,
                                                "Start": start,
                                                "End": end,
                                        "Description": "Dollyball2"})                                        
        
        qNo1 = Booking.objects.filter(location=location.id, start=start, end=end, description="Dollyball")
        qNo2 = Booking.objects.filter(location=location.id, start=start, end=end, description="Dollyball2")
        print(qNo1)
        self.assertGreater(qNo1[:1].get(), qNo2[:1].get())
        