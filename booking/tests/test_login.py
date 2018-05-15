from django.test import TestCase, Client
from accounts.models import User

class test_superuser_pass(TestCase):
    def setUp(self):
        mail = "supermanuser@heromail.com"
        pswrd = "clarKent123"
        User.objects.create_superuser(email=mail, password=pswrd)
        
