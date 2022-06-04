from ninja import Router
from typing import List
from lodge_app_apis.schema import *
from lodge_app.models import ReservedRoom, Reservation
from lodge_app_apis.controller.UserManagement import UserManagement
from lodge_app_apis.controller.BookingManagement import BookingManagement

api = Router()


@api.get("/reservation/myReservations")
def getMyReservations(request):
    pass


@api.post("/login", tags=["Login"])
def login(request, user: UserSchema):
    return UserManagement.login(request, user)


@api.get("/reservation/active")
def getActiveReservation(request):
    pass

@api.get("reservation/expired")
def getExpiredReservation(request):
    pass

@api.get("/booking/freeRooms")
def freeRooms(request):
     pass

@api.get("/booking/booked")
def bookedRooms(request):
    print("content")
    reservedRooms = ReservedRoom.objects.filter(reservation__active = True).all().count()

    print("Total reserved rooms is: "+str(reservedRooms))
    reservation = Reservation.objects.filter(active = True).first().reserved_rooms.all()
    rooms = []
    for room in reservation:
        js = {
            "name" : room.room.name,
            "number" : room.room.number
        }
        rooms.append(js)
    import json
    return json.dumps(rooms)
    print(reservation)
    return "no content"
    #return BookingManagement.bookedRooms(request)

@api.get("/booking/book")
def bookedRooms(request,booking: BookingSchema):
    return BookingManagement.bookRoom(request, booking)

@api.post("/reject/booking")
def rejectBooking(request, bookingId: int):
    return BookingManagement.rejectBooking(request, bookingId)

@api.post("/accept/booking")
def acceptBooking(request, bookingId: int):
    return BookingManagement.acceptBooking(request, bookingId)
