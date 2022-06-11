from datetime import datetime
from doctest import FAIL_FAST
from email.policy import default
import json
from math import fabs

import string

from multiprocessing import context
import re
from subprocess import check_output
from tabnanny import check
from unicodedata import name
from webbrowser import get
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.db.models import Q

from utils.utilities import is_ajax, reservation_code_generator
import uuid

from . models import  *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator


# Create your views here.

def index(request):
    user = request.user if type(request.user) is not AnonymousUser else None
    try:
        rooms = Room.objects.filter(published=True, booked=False).order_by('-created_at')
        my_booked_rooms = Reservation.objects.filter(guest=user )
        lodge = Lodge.objects.all().first()
        polices= Policy.objects.all()
        context = {
            'our_best_rooms': rooms,
            'my_booked_rooms': my_booked_rooms,
            'lodge': lodge,
            'polices': polices
        }
        return render(request, template_name='index.html', context=context)

    except:
        rooms = Room.objects.filter(published=True, booked=False).order_by('-created_at')
        lodge = Lodge.objects.all().first()
        polices= Policy.objects.all()

        print(lodge)
        context = {
            'our_best_rooms': rooms,
             'lodge': lodge,
           'polices': polices
        }
        return render(request, template_name='index.html', context=context)
            
   
def room(request):
    rooms = Room.objects.all()
    amenities = Amenity.objects.all()

    lodge = Lodge.objects.all().first()
    paginator = Paginator(rooms, 2) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'rooms': page_obj,
        'amenities': amenities,
        'lodge': lodge,

    }
    return render(request, template_name='rooms.html', context=context)

class RoomDetails(View):
    def get(self, request, pk, *args, **kwargs):
        room = Room.objects.get(id = pk)
        user = request.user if type(request.user) is not AnonymousUser else None
        print(room.get_room_images())
        lodge = Lodge.objects.all().first()

        polices= Policy.objects.all()
        try:
            my_booked_rooms = Reservation.objects.filter(guest=user)
            context = {
            'room_details': room,
            'my_booked_rooms': my_booked_rooms,
            'lodge': lodge,
           'polices': polices
            }
            return render(request, template_name='room_details.html', context=context)
        except :
            context = {
            'room_details': room,
            'lodge': lodge,
           'polices': polices
            }
            return render(request, template_name='room_details.html', context=context)

    def post(self, request,  pk , *args, **kwargs ):
         if is_ajax(request) and request.POST.get('action') == 'search_room_and_save':
            booked_room_id = request.POST.get('booked_room_id')
            check_in = request.POST.get('check_in')
            _first_name = request.POST.get('first_name')
            _last_name = request.POST.get('last_name')
            _phone = request.POST.get('phone')
            check_out = request.POST.get('check_out')
            chosen_room =  request.POST.get('booked_room_name')


            print(booked_room_id)
            # try:
            guest, created = Guest.objects.get_or_create(
                first_name=_first_name,
                last_name = _first_name,
                phone = _phone
            )
            print(guest)
            room= Room.objects.get(id=booked_room_id)
            reserving_model, created = Reservation.objects.get_or_create(room = room, guest_id=guest.id)
            reverved_rooms, created = ReservedRoom.objects.get_or_create(reservation=reserving_model, room=room, )
            if room.booked==False and reserving_model.comfirmed==False:
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
                    'msg': f'You have successfully made a booking {chosen_room} with {reserving_model.reservation_code} reservation code'
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
    if request.POST.get('action') == 'comfirm_booking':
        reservation_id =  request.POST.get('reservation_id')
        room_id =  request.POST.get('room_id')
        _room = Room.objects.get(id=room_id)
        booking_model= Reservation.objects.get(room = _room, id =reservation_id)
        if _room.booked ==True:
            response = {
                'msg':f'you delayed in comfirming the Booking. Already taken'
            }
            return JsonResponse(response)
        else:
         
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
        reservation_id =  request.POST.get('reservation_id')
        room_id =  request.POST.get('room_id')
        _room = Room.objects.get(id=room_id)
        booking_model= Reservation.objects.get(room = _room, id =reservation_id)

        booking_model.comfirmed =False
        booking_model.canceled =True
        booking_model.save()

        _room .booked = False
        _room .save()
        response = {
                    'msg':f'Booking is conceled successifully'
            }
        return JsonResponse(response)
    

def searchReservation(request):
    check_in = request.POST.get('check_in')
    check_out = request.POST.get('check_out')
    phone=  request.POST.get('phone')

    res_code = request.POST.get('res_code')
    reservation_list = []
    print(f'====>{check_out} \n, ====> {check_in}\n, ===>{res_code}')
    
    queryset = Reservation.objects.filter(reservation_code = res_code, guest__phone =phone )
    print(queryset)
    serializer =serializers.serialize('json', queryset)
  
    for data in queryset:
        reservation_obj={
            'res_id':data.id,
            'room_image': data.room.thumbnail.url,
            'room_name': data.room.name,
            'room_id': data.room.id,
            'room_status': data.room.booked,
            'date_in':data.date_in, 
            'date_out': data.date_out,
            'res_code':data.reservation_code,
            'comfirmed':data.comfirmed,
            'canceled':data.canceled
            }
        reservation_list.append(reservation_obj)

    response = {
        'detailed_qs':json.dumps(reservation_list,default=str),
        'query_set': serializer,
        'msg':f'read to go'
        }

    return JsonResponse(response)