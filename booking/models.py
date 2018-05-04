from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from groups.models import SportsGroup
from groups.models import Membership
from django.contrib.auth.models import User
from django.db.utils import OperationalError

LOCATION_TYPES = (
    ('gym ', 'GYM'),
    ('football field', 'FOOTBALL FIELD'),
    ('volleyball grounds', 'VOLLEYBALL GROUNDS')
)


#Location model
class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    type = models.CharField(max_length=200, choices=LOCATION_TYPES, default='gym')

    def __str__(self):
        return self.name

#Booking model
class Booking(models.Model):
    person = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=400, default='')
    description = models.CharField(max_length=400, default='')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    start = models.DateTimeField(_(u'Start'), blank=True)
    end = models.DateTimeField(_(u'End'), blank=True)
    queueNo = models.IntegerField(default=0)

    try:
        tu = tuple(SportsGroup.objects.all().values_list('name', 'name'))
        if not tu:
            tu = (
                ('', '---------'),
            )
        else:
            tu = tuple(SportsGroup.objects.all().values_list('name', 'name'))

    except OperationalError:
        tu = (
            ('', '---------'),
        )

    group = models.CharField(max_length=200, blank=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('booking_edit', kwargs={'pk': self.pk})

    
    def save(self, *args, **kwargs):
        #TODO: editing causes interference with its own old qNo value
        # compare to all with qNo=0
        # a|----| b|----|
        #    c|-----| d|---|
        #               e|----|
        # c overlaps with a and b, put c.qNo = 1
        # d overlaps with b, put d.qNo = 1
        # e overlaps with d, put eqNo = 0
        
        bookings = Booking.objects.filter(location=self.location, start__lt=self.end, end__gt=self.start)
        first = bookings.filter(queueNo=0)
        if list(first) != []:
            # print(bookings)
            print("before save: ", self.queueNo)
            maxval = bookings.aggregate(models.Max('queueNo'))
            temp = [maxval [i] for i in sorted(maxval.keys())]
            self.queueNo = int(temp[0])+1
            print("after save: ", self.queueNo)
            print(first[0])
            print(self)
            if first[0] == self:
                self.queueNo = first[0].queueNo
        else:
            self.queueNo = 0
        return super(Booking, self).save(*args, **kwargs)


    
    def delete(self, *args, **kwargs):
        qNo = self.queueNo
        #find overlapping bookings
        bookings = Booking.objects.filter(location=self.location, start__lt=self.end, end__gt=self.start)
        #find bookings which are later in queue
        later = bookings.filter(queueNo__gt=qNo)
        for i in range(len(later)):
            if later[i].queueNo > 0:
                c = later[i]
                c.queueNo -= 1
                print("reduced: ", c.queueNo)
                super(Booking, c).save()
                # if c.queueNo == 0:
                    # msg = "You have now booked " + c.location+ ", from "+ c.start+ " to "+ c.end
                    # #sendMail(msg)
                    # print(msg)
                # else:
                    # msg = "You are now number "+ c.queueNo+ " in line for "+ c.location+ " starting "+ c.start
                    # #sendMail(msg)
                    # print(msg)
            #later[i].save()
        # user = "user"
        # msg = "your booking for "+ self.location+ " starting "+ self.start+ " has been deleted by "+ user
        # #sendmail(msg)
        # print("your booking for "+ self.location+ " starting "+ self.start+ " has been deleted by "+ user)
        return super(Booking, self).delete(*args, **kwargs)
    

    def get_groups(self):
        memberships = Membership.objects.filter(person=self.person).values_list('group', flat=True)
        my_groups = []
        for m in memberships:
            sport_groups = SportsGroup.objects.get(id=m).name
            my_groups.append(sport_groups)
        return my_groups

    def get_date(self):
        start = self.start
        end = self.end
        day = start.strftime("%A")
        date = start.strftime("%d %B")
        start_time = start.strftime("%H:%M")
        end_time = end.strftime("%H:%M")
        dates = (day, date, start_time, end_time)
        return dates
