from unicodedata import name
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import views
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.index, name='home'),
    path('room_details/<int:pk>', views.RoomDetails.as_view() ,name= 'room_details' ),
    path('manageBookingstatus', views.manageBookingStatus, name= 'manageBookingstatus' ),
    path('search-reservation', views.searchReservation, name= "search-reservation"),
    path('rooms', views.room , name='rooms')
]
