from lodge_app.models import *
from django.contrib.auth import authenticate


class BookingManagement:
    def bookedRooms(request, hotel_id : int):
        try:
            return {
                "message": "Successfully booked a room",
                "code": 200
            }
        except Exception as e:
            return {
                "message": "Unknown error occured while rendering your request",
                "code": 2200
            }

    def bookRoom(request, bookRoomSchema):
        try:
            return {
                "message": "Successfully booked a room",
                "code": 200
            }
        except Exception as e:
            return {
                "message": "Unknown error occured while rendering your request",
                "code": 2200
            }
