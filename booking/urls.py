from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='booking'),
    url(r'^api', views.api, name='api'),
    url(r'^profile', views.BookingList.as_view(), name='booking_list'),
    url(r'^new$', views.BookingCreate.as_view(), name='booking_new'),
    url(r'^edit/(?P<pk>\d+)$', views.BookingUpdate.as_view(), name='booking_confirm_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.BookingDelete.as_view(), name='booking_delete'),
    url(r'^create/$', views.NewsCreateView.as_view(), name='news-create'),
    url(r'^all/', views.BookingAll, name="booking_all_list"),
]
