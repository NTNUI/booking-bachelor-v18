from django.test import TestCase, Client
from accounts.models import User
from booking.models import Location, Booking
#from booking.views import repeatBooking
from datetime import datetime, time
from calendar import Calendar
class test_recurring(TestCase):

    def setUp(self):
        loc = Location(name="snaicfield")
        loc.save()
        self.data = {
            "start":datetime(2018, 4, 30, 12),
            "end":datetime(2018, 4, 30, 15),
            "location": loc,
            "title":"2fast5u",
            "description":"gottagofast"
        }
    
    def test_repeat(self):
        # b_list = self.repeatBooking(self.data)
        # print(b_list)
        self.assertTrue(False)
    
    def test_repeatBooking(self, repeat=True):
        dayofweek = 0# day_map[form.cleaned_data['dayID'].upper()]
        cleaned_data = self.data
        start = cleaned_data['start']
        end = cleaned_data['end']
        year = int(start.year)
        month = int(start.month)
        day = int(start.day)#[8:10])
        loc = cleaned_data['location']
        s_time = str(start)[-8:] #get time substring
        e_time = str(end)[-8:]
        title = cleaned_data['title']
        descr = cleaned_data['description']
        b_list = []
        
        if True:
            cal = Calendar()
            ydcal = cal.yeardays2calendar(year, width=6)
            if month > 5:
                w = ydcal[1]
            else:
                w = ydcal[0]
            for m in range(len(w)):
                if m+1 < month:
                    continue #skip past months 
                for k in range(len(w[m])): #week in a month
                    for d in range(len(w[m][k])): #days in a week
                        cal_day = w[m][k][d]
                        if (cal_day[0] < day and m+1 == month) or cal_day[0]==0:
                            continue
                        if cal_day[1]==dayofweek:
                            # print("here")
                            if m <9: #format month
                                cal_m = "0"+str(m+1)
                            else:
                                cal_m = str(m+1)
                            if cal_day[0]<9: #format day
                                cal_d = "0"+str(cal_day[0])
                            else:
                                cal_d = str(cal_day[0])
                            date_format = str(year)+"-"+cal_m+"-"+cal_d 
                            start_rec = date_format+" "+s_time
                            end_rec = date_format+" "+e_time
                            b = Booking(location=loc, start=start_rec, end=end_rec, title=title, description=descr)
                            b.save()
                            b_list.append(b)
        self.assertTrue(False)
        return b_list
