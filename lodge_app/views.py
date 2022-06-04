from django.shortcuts import render
from .models import Room, Amenity

# Create your views here.

def index(request):
    # rooms = Room.objects.filter(published=True).order_by('-created_at')
    context = {
         'our_best_rooms': 'hello'
    }
    return render(request, template_name='hotel_app/index.html', context=context)




#
# def index(request):
#     rooms = Room.objects.all()
#     print(rooms)
#     context = {
#         "rooms": rooms
#     }
#     return render(request, "hotel_app/index.html", context)
#
# def about(request):
#     rooms = Room.objects.all()
#     print(rooms)
#     context = {
#         "rooms": rooms
#     }
#     return render(request, "hotel_app/about.html", context)
#
#
# def bookRoom(request):
#     pass
#
# def viewMyBookings(request):
#     pass
#
#
# def rooms(request):
#     rooms = Room.objects.all()
#     context = {
#         "rooms": rooms
#     }
#     return render(request, "hotel_app/blog.html", context)
#
#
# def roomDetail(request, room_id):
#     room = Room.objects.get(id = room_id)
#     context = {
#         "room": room
#     }
#     return render(request, "hotel_app/room-details.html", context)
#
#
# def amenities(request):
#     amenities = Amenity.objects.all()
#     print(amenities)
#     context = {
#         "amenities": amenities
#     }
#     return render(request, "hotel_app/aminities.html", context)
