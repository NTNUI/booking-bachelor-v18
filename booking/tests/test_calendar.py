from django.conf import settings
from ntnui.tests.browser.lib.browser_test_case import ChromeTestCase, FirefoxTestCase
from ntnui.tests.browser.lib.helpers import login_user
from selenium.webdriver.support.wait import WebDriverWait
from groups.models import Invitation, SportsGroup
from accounts.models import User
from selenium import webdriver
from booking.models import Booking, Location
from django.contrib.staticfiles.testing import StaticLiveServerTestCase, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('myuser')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('secret')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()






def see_calendar(cls, browser):
    browser.get(cls.server_url + '/booking')
    gym = browser.find_element_by_id('gym')
    gym.click()
    filtering = browser.find_elements_by_xpath('//input[@name="opradio" and @value="GymName"]')[0]
    filtering.click()
    current_loc = browser.find_element_by_id('current-location')
    cls.assertEqual('GymName', current_loc.get_attribute('innerHTML').trim())


def see_booked(cls, browser):
    browser.get(cls.server_url + '/booking')
    gym = browser.find_element_by_id('gym')
    gym.click()
    filtering = browser.find_elements_by_xpath('//input[@name="opradio" and @value="GymName"]')[0]
    filtering.click()
    current_loc = browser.find_element_by_id('current-location')
    day = browser.find_element_by_id(cls.date)
    day.click()
    booked_by = browser.find_element_by_xpath('//input[@class="card-body 3" and @title="Click to see your booking"')
    author = Booking.objects.filter(start=cls.date+' 12:00')[0].person
    cls.assertEqual(booked_by, author)
    
def profile_bookings(cls, browser):
    browser.get(cls.server_url+'/')

def create_booking(cls, browser):
    browser.get(cls.server_url + '/booking')
    gym = browser.find_element_by_id('gym')
    gym.click()
    filtering = browser.find_elements_by_xpath('//input[@name="opradio" and @value="GymName"]')[0]
    filtering.click()
    current_loc = browser.find_element_by_id('current-location')
    day = browser.find_element_by_id(cls.date)
    day.click()
    title = browser.find_element_by_id('id_title')
    title.send_keys('new booking')
    desc = browser.find_element_by_id('id_description')
    desc.send_keys('description for new booking')
    desc.send_keys(Keys.RETURN)
    booking = Booking.objects.filter(title='new booking')[0]
    cls.assertTrue(booking.description=='description for new booking')


class CalendarChrome(ChromeTestCase):
    fixtures = ['users.json', 'groups.json', 'membership.json', 'board.json']

    def setUp(self):
        self.loc = Location.objects.create(name='GymName', address='123 st', description='best gym')
        self.date = '2018-06-10'
        Booking.objects.create(location=self.loc, title='Jump', description='Jump around', start=self.date+' 12:00', end=self.date+' 13:00')
        login_user(self, self.chrome)

    def test_see_calendar(self):
        see_calendar(self, self.chrome)
    
    def test_create_booking(self):
        see_booked(self, self.chrome)


class CalendarFirefox(FirefoxTestCase):
    fixtures = ['users.json', 'groups.json', 'membership.json', 'board.json']

    def setUp(self):
        self.loc = Location.objects.create(name='GymName', address='123 st', description='best gym')
        self.date = '2018-06-10'
        Booking.objects.create(location=self.loc, title='Jump', description='Jump around', start=self.date+' 12:00', end=self.date+' 13:00')
        login_user(self, self.firefox)

    def test_see_calendar(self):
        see_calendar(self, self.firefox)
        
    def test_create_booking(self):
        see_booked(self, self.firefox)


