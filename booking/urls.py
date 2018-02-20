from django.conf.urls import include, url
from . import views

urlpatterns = [
    url('', views.index, name='booking'),
    url(r'^$', views.BookingList.as_view(), name='booking_list'),
    url(r'^new$', views.BookingCreate.as_view(), name='booking_new'),
    url(r'^edit/(?P<pk>\d+)$', views.BookingUpdate.as_view(), name='booking_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.BookingDelete.as_view(), name='booking_delete'),

]
