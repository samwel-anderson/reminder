from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from . import views
from django.conf import settings
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.index, name='home'),
    path('room_details/<int:pk>', views.RoomDetails.as_view() ,name= 'room_details' ),
    path('booking_system/<int:pk>', views.BookingSytem.as_view() ,name= 'booking_system'),
    path('manageBookingstatus', views.manageBookingStatus, name= 'manageBookingstatus' )

    # path('', RedirectView.as_view(url="/")),
    # path('index/',views.index, name = "index"),
    # path('amenities/',views.amenities, name = "amenities"),
    # path('rooms/',views.rooms, name = "rooms"),
    # path('room/detail/<int:room_id>',views.roomDetail, name = "roomDetail"),
    # path('about/',views.about, name = "about"),
    # path('about/',views.about, name="about"),
    # path('post_detail/<post_id>',views.post_detail, name="post_detail"),
    # path("post_data/<slug>",views.friendly_post_detail,name="post_data"),
    # path("posts/category_id",views.posts,name="posts"),
    # path("category/<category_id>",views.posts,name="category"),
    # path("categories/",views.post_categories, name="categories"),
    # path("downloads/",views.downloads,name="downloads"),
]
