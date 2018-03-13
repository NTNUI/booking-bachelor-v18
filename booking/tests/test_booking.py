from django.test import TestCase, Client
import datetime
from accounts.models import User
from booking.models import Booking



class test_create_booking(TestCase):
    
    def setUp(self):
        mail = "goodboy@mail.com"
        passwrd = "pass123"
        User.objects.create_user(email=mail, password=passwrd)
        # User.objects.create_user
        self.c = Client()
        self.c.login(email=mail, password=passwrd)
    
    def test_valid_booking(self):
        response = self.c.post("/booking/create/", {'location': 'Idrettshallen', 'Start': '05.03.2018', 
                        'End': '06.03.2018', 'Description': 'Paryoga'})
        self.assertTemplateUsed(response, "booking/booking_form.html")
        self.assertEquals(response.status_code, 200)

    def test_time_travel(self):
        #test end before start
        #self.assertFieldOutput(EmailField, {'a@a.com': 'a@a.com'}, {'aaa': ['Enter a valid email address.']})
        response = self.c.post("/booking/create/", {'location': 'Idrettshallen', 'Start': '05.03.2018', 
                        'End': '04.03.2018', 'Description': 'Paryoga'})
        self.assertEquals(response.status_code, 400)
        #test start before today    
        now = datetime.datetime.now()
        now_str =  ""+now.day+"."+now.month+"."+now.year
        response = self.c.post("/booking/create/", {'location': 'Idrettshallen', 'Start': now_str, 
                        'End': '04.03.2018', 'Description': 'Paryoga'})
        self.assertEquals(response.status_code, 400)
    
    def test_double_booking(self):
        #TODO: retrieve stored bookings from database, post data, assert response equals
        booking = Booking.objects.all()[0]
        #create double booking
        response = self.c.post("/booking/create/", {'location': str(booking.location), 'Start': 
                        str(booking.start), 'End': str(booking.end), 'Description': str(booking.description)})
        self.assertEquals(response.status_code, 400) 



class test_delete(TestCase):
    
    def setUp(self):
        mail = "goodboy@mail.com"
        passwrd = "pass123"
        User.objects.create_user(email=mail, password=passwrd)
        self.c = Client()
        self.c.login(email=mail, password=passwrd)

    # get request for popup "GET /booking/new HTTP/1.1" 200 732
    


    def test_delete_booking(self):

        #create booking
        response = self.c.post("/booking/create/", {'location': 'Idrettshallen', 'Start': '05.03.2018', 
                        'End': '06.03.2018', 'Description': 'Paryoga'})
        self.assertTemplateUsed(response, "booking/booking_form.html")
        self.assertEquals(response.status_code, 200)
        #delete booking
        response = self.c.post("booking/delete")

    #c.post
    pass