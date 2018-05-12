from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='booking'),
    url(r'^api', views.api, name='api'),
    url(r'^location_api', views.location_api, name='api'),
    url(r'^hours_api', views.api2, name='api2'),
    url(r'^profile', views.BookingList.as_view(), name='booking_list'),
    url(r'^all/', views.booking_all, name="booking_all_list"),
    url(r'^bookings_list/$', views.booking_list, name='booking_list'),
    url(r'^bookings_list/create/$', views.booking_create, name='booking_create'),
    url(r'^bookings_list/create_calendar/$', views.booking_create_from_calendar, name='booking_create_calendar'),
    url(r'^books/(?P<pk>\d+)/update/$', views.booking_update, name='booking_update'),
    url(r'^books/(?P<pk>\d+)/delete/$', views.booking_delete, name='booking_delete'),

    url(r'^booking_confirm/(?P<pk>\d+)/$', views.booking_confirm, name='booking_confirm'),
    url(r'^delete_request/(?P<pk>\d+)/$', views.delete_request, name="delete_request"),

]
