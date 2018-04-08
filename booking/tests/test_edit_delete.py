from django.test import TestCase, Client
from accounts.models import User
from booking.models import Booking, Location

class test_enqueue(TestCase):

    def setUp(self):
        mail = "test@example.com"
        pswrd = "TestyTest123"
        User.objects.create_superuser(email=mail, password=pswrd)
        self.login_response = self.client.login(email=mail, password=pswrd)
        ##
        self.loc = "Idrettshallen"
        Location.objects.create(name=self.loc)
        self.location = Location.objects.get(name=self.loc)
        self.start = "2018-04-15 10:00:00"
        self.s1 = self.start
        self.s2 = "2018-04-15 12:50:00"
        self.s3 = "2018-04-15 13:01:00"
        self.end = "2018-04-15 13:00:00"
        self.e1 = self.end
        self.e2 = "2018-04-15 14:00:00"
        self.e3 = "2018-04-15 15:00:00"
        self.url = "/booking/bookings_list/create/"
        self.d1 = "Dollyball"
        self.d2 = "Dollyball2"
        self.d3 = "Dollyball3"

    def test_enqueued(self):                                      
        Booking.objects.create(location=self.location, start=self.start, end=self.end, description=self.d1)
        Booking.objects.create(location=self.location, start=self.start, end=self.end, description=self.d2)
        qNo1 = Booking.objects.filter(location=self.location, start=self.start, end=self.end, description=self.d1)
        qNo2 = Booking.objects.filter(location=self.location, start=self.start, end=self.end, description=self.d2)
        print(qNo1[:1].get().queueNo)
        print(qNo2[:1].get().queueNo)
        for i in range(len(qNo1)):
            print(qNo1[i])
        self.assertGreater(qNo2[0].queueNo, qNo1[0].queueNo)
        self.assertTrue(False)
    
    def test_multi_enq(self):   
        #create bookings in database                                  
        Booking.objects.create(location=self.location, start=self.start, end=self.end, description=self.d1)
        Booking.objects.create(location=self.location, start=self.s2, end=self.e2, description=self.d2)
        Booking.objects.create(location=self.location, start=self.s3, end=self.e3, description=self.d3)
        #retrieve bookings from database
        qNo1 = Booking.objects.filter(location=self.location, start=self.start, end=self.end, description=self.d1)
        qNo2 = Booking.objects.filter(location=self.location, start=self.s2, end=self.e2, description=self.d2)
        qNo3 = Booking.objects.filter(location=self.location, start=self.s3, end=self.e3, description=self.d3)
        # qNo3 = Booking.objects.filter(location=location, )
        print(qNo1[:1].get().queueNo)
        print(qNo2[:1].get().queueNo)
        print(qNo3[:1].get().queueNo)
        #Test if booking 1 is before booking 2 in queue
        self.assertGreater(qNo2[:1].get().queueNo, qNo1[:1].get().queueNo)
        #test if booking 3 is before booking 2 in queue
        self.assertGreater(qNo2[:1].get().queueNo, qNo3[:1].get().queueNo)

    def test__post_enq(self):
        
        response = self.client.post(self.url, {"location": self.location,
                                                "Start": self.start,
                                                "End": self.end,
                                                "Description": self.d1})
        qNo1 = Booking.objects.filter(location=self.location, start=self.start, end=self.end, description=self.d1)                                                
        print(Booking.objects.all())
        print(response)
        self.assertTrue(False)
    
    def test_delete(self):
        date = "2018-04-15 "
        s1 = date+ "12:00:00"
        s2 = date+ "11:00:00"
        s3 = date+"13:00:00"
        e1 = date+"14:00:00"
        e3 = date+"15:00:00"
        #create bookings
        Booking.objects.create(location=self.location, start=s1, end=e1, description=self.d1)
        Booking.objects.create(location=self.location, start=s2, end=s3, description=self.d2)
        Booking.objects.create(location=self.location, start=s3, end=e3, description=self.d3)
        #before
        print("before")
        b2 = Booking.objects.filter(location=self.location, start=s2, end=s3, description=self.d2)[0]
        b3 = Booking.objects.filter(location=self.location, start=s3, end=e3, description=self.d3)[0]
        print(b2.queueNo)
        print(b3.queueNo)
        #delete first booking
        b1 = Booking.objects.filter(location=self.location, start=s1, end=e1, description=self.d1)[0]
        b1.delete()
        #check if later bookings ahve updated queueNo
        print("after")
        b2 = Booking.objects.filter(location=self.location, start=s2, end=s3, description=self.d2)[0]
        b3 = Booking.objects.filter(location=self.location, start=s3, end=e3, description=self.d3)[0]
        # print(Booking.objects.all())
        print(b2.queueNo)
        print(b3.queueNo)
        self.assertTrue(False)

    def test_edit(self):
        b1 = Booking(location=self.location, start=self.s1, end=self.e1, description=self.d1)
        b1.save()
        b2 = Booking(location=self.location, start=self.s2, end=self.e2, description=self.d2)
        b2.save()
        qNo1 = b2.queueNo
        #update second booking
        b2.start = self.s3
        b2.start = self.e3
        b2.save()
        qNo2 = b2.queueNo
        print("before ", qNo1)
        print("after", qNo2)
        self.assertTrue(False)
    
    def test_edit_inplace(self):
        s1 = "2018-05-15 12:00:00"
        s2 = "2018-05-15 13:00:00"
        s3 = s1
        s4 = "2018-05-15 16:00:00"
        e1 = "2018-05-15 17:00:00"
        e2 = "2018-05-15 14:00:00"
        e3 = "2018-05-15 15:00:00"
        Booking.objects.create(location=self.location, start=s1, end=e1, description="first")
        b2 = Booking(location=self.location, start=s2, end=e2, description="second")
        b2.save()
        b3 = Booking(location=self.location, start=s3, end=e3)
        print(b2.start.date)
        self.assertTrue(False)


        
