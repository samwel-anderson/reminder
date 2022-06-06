from datetime import datetime
from doctest import FAIL_FAST
import json
from math import fabs

import string

from multiprocessing import context
import re
from tabnanny import check
from unicodedata import name
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from utils.utilities import is_ajax, reservation_code_generator
import uuid

from . models import  *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

# Create your views here.

def index(request):
    user = request.user if type(request.user) is not AnonymousUser else None
    try:
        rooms = Room.objects.filter(published=True, booked=False).order_by('-created_at')
        my_booked_rooms = Reservation.objects.filter(guest=user)
        context = {
            'our_best_rooms': rooms,
            'my_booked_rooms': my_booked_rooms
        }
        return render(request, template_name='index.html', context=context)

    except:
        rooms = Room.objects.filter(published=True, booked=False).order_by('-created_at')
        context = {
            'our_best_rooms': rooms,
        }
        return render(request, template_name='index.html', context=context)
            
   

class RoomDetails(View):
    def get(self, request, pk, *args, **kwargs):
        room = Room.objects.get(id = pk)
        user = request.user if type(request.user) is not AnonymousUser else None
      

        try:
            my_booked_rooms = Reservation.objects.filter(guest=user)
            context = {
            'room_details': room,
            'my_booked_rooms': my_booked_rooms
            }
            return render(request, template_name='room_details.html', context=context)
        except :
            context = {
            'room_details': room,
           
            }
            return render(request, template_name='room_details.html', context=context)

    def post(self, request,  pk , *args, **kwargs ):
      
         if is_ajax(request) and request.POST.get('action') == 'search_room_and_save':
           
            booked_room = request.POST.get('booked_room')
            check_in = request.POST.get('check_in')
            check_out = request.POST.get('check_out')
            chosen_room =  request.POST.get('change_room')
            
            
            # try:
            room = Room.objects.get(name=chosen_room)
            reserving_model, created = Reservation.objects.get_or_create(room = room, guest_id = request.user.id)
            reverved_rooms, created = ReservedRoom.objects.get_or_create(reservation=reserving_model, room=room)
            if reserving_model.comfirmed==False:
                    reserving_model.user = request.user
                    reserving_model.room = room
                    reserving_model.date_in = check_in
                    reserving_model.reservation_code =  uuid.uuid4()
                    reserving_model.date_out =  check_out
                    reserving_model.save()
                
                    response = {
                    'room_booked': {
                        "user": str(reserving_model.guest),
                        'room': str(reserving_model.room.name),
                        'room_image': str(reserving_model.room.thumbnail.url),
                        "check_in": reserving_model.date_in,
                        "check_out": reserving_model.date_out ,
                        "price": reserving_model.room.price,
                        'r_code': reserving_model.reservation_code,
                        'room_image_list': json.dumps( reserving_model.room.get_room_images() )
                    },
                    'msg': f'Your Search for {chosen_room} room has been made successfully ,you were able to book  for it'
                    }
                    return JsonResponse(response,safe=False)
                
            elif reserving_model.guest == request.user and reserving_model.comfirmed==False :
                response = {
                    'room_booked': {
                        "user": str(reserving_model.guest),
                        'room': str(reserving_model.room.name),
                        'room_image': str(reserving_model.room.thumbnail.url),
                        "check_in": reserving_model.date_in,
                        "check_out": reserving_model.date_out,
                        "price": reserving_model.room.price,
                        'r_code': reserving_model.reservation_code,
                        'room_image_list': json.dumps( reserving_model.room.get_room_images() )
                    },
                    'msg': f'You already booked for {chosen_room}  Go head to confirm booking'
                    }
                return JsonResponse(response)
            else:
                response = {
                    'msg': f'The room is not avilable or already booked for it. Go to you profile to see a list of booked rooms'
                }
                return JsonResponse(response)
            # except:
            #     response = {
            #             'msg':f'We have no such type of room, Or You\'re missing some information for your search'
            #     }
            #     return JsonResponse(response)


           
def manageBookingStatus(request):
    print(request.POST)
    print(request.POST.get('action') == 'comfirm_booking')
    if request.POST.get('action') == 'comfirm_booking':
        chosen_room =  request.POST.get('origin_room')
        _room = Room.objects.get(name=chosen_room)
        booking_model= Reservation.objects.get(room = _room, guest = request.user)

        booking_model.comfirmed = True
        booking_model.canceled = False
        booking_model.save()

        _room .booked = True
        _room .save()
        response = {
                    'msg':f'Booking conformed'
            }
        return JsonResponse(response)

    else:
        chosen_room =  request.POST.get('origin_room')
        _room  = Room.objects.get(name=chosen_room)
        booking_model= Reservation.objects.get(room = _room , guest = request.user)

        booking_model.comfirmed =False
        booking_model.canceled =True
        booking_model.save()

        _room .booked = False
        _room .save()
        response = {
                    'msg':f'Booking is conceled successifully'
            }
        return JsonResponse(response)
    
