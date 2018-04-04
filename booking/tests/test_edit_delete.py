from django.test import TestCase, Client
from accounts.models import User
from booking.models import Booking, Location

class test_enqueue(TestCase):

    def setUp(self):
        mail = "test@example.com"
        pswrd = "TestyTest123"
        User.objects.create_superuser(email=mail, password=pswrd)
        # self.login_response = self.client.login(email=mail, password=pswrd)
        # #
        self.c = Client()
        self.c.login(email=mail, password=pswrd)
        Location.objects.create(name="Idrettshallen")
        
    def test_g(self):
        self.assertGreater(2, 1)

    def test_enqueue_func(self):
        loc = "Idrettshallen"
        location = Location.objects.get(name=loc)
        start = "2018-04-15 10:00:00"
        end = "2018-04-15 13:00:00"
        url = "/booking/bookings_list/create"                                      
        Booking.objects.create(location=location, start=start, end=end, description="Dollyball")
        Booking.objects.create(location=location, start=start, end=end, description="Dollyball2")
        qNo1 = Booking.objects.filter(location=location, start=start, end=end, description="Dollyball")
        qNo2 = Booking.objects.filter(location=location, start=start, end=end, description="Dollyball2")
        self.assertGreater(qNo2[:1].get().queueNo, qNo1[:1].get().queueNo)

    # def test_enqueued(self):
    #     loc = "Idrettshallen"
    #     location = Location.objects.get(name=loc)
    #     start = "2018-04-15 10:00:00"
    #     end = "2018-04-15 13:00:00"
    #     url = "/booking/bookings_list/create"
    #     response = self.c.post(url, {"location": location,
    #                                             "Start": start,
    #                                             "End": end,
    #                                             "Description": "Dollyball"})
    #     self.c.post(url, {"location": location,
    #                                             "Start": start,
    #                                             "End": end,
    #                                     "Description": "Dollyball2"})                                        
       
    #     print("locations: ", Booking.objects.values_list('location', flat=True))
        
    #     qNo1 = Booking.objects.filter(location=location, start=start, end=end, description="Dollyball")
    #     qNo2 = Booking.objects.filter(location=location, start=start, end=end, description="Dollyball2")
    #     print("qno: ", qNo1)
    #     self.assertGreater(qNo2[:1].get().queueNo, qNo1[:1].get().queueNo)
        