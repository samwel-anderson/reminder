from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

class Amenity(models.Model):
    name = models.CharField(max_length=50, null = False, blank = False)
    faIcon = models.CharField(max_length=50, null = False, blank = False)

    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"
        db_table = "hotel_amenity"


    def __str__(self):
        return self.name

class Hotel(models.Model):
    description = models.TextField(null = False, blank = False)
    name = models.CharField(max_length=200,null = False, blank = False)
    hotelRoomInfo = models.TextField(max_length=500, null = False, blank = False)

    class Meta:
        verbose_name = "Hotel"
        db_table = "hotel"

    def __str__(self):
        return self.name

class Freebie(models.Model):
    name = models.CharField(max_length = 200)
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE)

    class Meta:
        verbose_name = "freebie"
        verbose_name_plural = "freebies"
        db_table = "hotel_freebie"

    def __str__(self):
        return self.name

class HotelPhoto(models.Model):
    HOTEL_PHOTO_CHOICES = (
        ("BEDROOM", "Bedroom"),
        ("OTHER", "Other"),
        ("BUILDING", "Building"),
        ("LOBBY", "Lobby"),
    )
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE)
    date_uploaded = models.DateTimeField(auto_now_add = True)
    category = models.CharField(blank = False, null = False, choices =
    HOTEL_PHOTO_CHOICES, default="BEDROOM", max_length = 25)
    image = models.ImageField(null = False, blank = False)

    def  image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="60" height="60" />' % (self.image))

    image_tag.allow_tags = True

    class Meta:
        verbose_name = "Hotel Photo"
        verbose_name_plural = "Hotel photos"
        db_table = "hotel_photo"

    def __str__(self):
        return str(self.category) +str(" Photo of ") + str(self.hotel.name)

class HotelLocation(models.Model):
    location_name = models.CharField(max_length = 200, null = False, blank = False)
    latitude = models.DecimalField(blank = True, null = True, decimal_places = 8, max_digits = 50)
    longitude = models.DecimalField(blank = True, null = True, decimal_places = 8, max_digits = 50)
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE, null = True, blank = True)
    nearbyLocation = models.ForeignKey("self", on_delete = models.CASCADE, null = True, blank = True)

    class Meta:
        verbose_name = "Hotel Location"
        verbose_name_plural = "Hotel locations"
        db_table = "hotel_location"

    def __str__(self):
        return self.location_name

class Policy(models.Model):
    title = models.CharField(max_length = 50)
    description = models.TextField(max_length = 500)
    hotel = models.ForeignKey(Hotel, on_delete = models.CASCADE)

    class Meta:
        db_table = "hotel_policy"
        verbose_name = "Policy"
        verbose_name_plural = "Policies"

    def __str__(self):
        return self.title

class Reservation(models.Model):
    date_in = models.DateTimeField(auto_now_add = False, blank = False)
    date_out = models.DateTimeField(blank = False, null = False)
    active = models.BooleanField(default = False)
    staff_activated = models.ForeignKey(User, on_delete = models.CASCADE)
    guest = models.ForeignKey("Guest", on_delete = models.CASCADE)

    def __str__(self):
        return str(self.date_in) + str(self.date_out) + str(self.active)

class ReservedRoom(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete = models.CASCADE)
    room = models.ForeignKey("Room", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name = "Rerseved Room"
        verbose_name_plural = "Reserved Rooms"
        db_table = "hotel_reserved_room"

class Guest(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 15)
    updated_at = models.DateTimeField(auto_now = True)
    address = models.CharField(max_length = 100, null = True, blank = True)
    member_since = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = "Guest"
        verbose_name_plural = "Guests"
        db_table = "hotel_guest"

    def __str__(self):
        return self.first_name + " "+str(self.last_name) + " Phone: "+self.phone

class Room(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length = 50)
    price = models.DecimalField(max_digits = 12, decimal_places = 2)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        db_table = "hotel_room"


    def __str__(self):
        return "Room Number {0} which named: {1}".format(self.number, self.name)

class RoomPhoto(models.Model):
    image = models.ImageField(upload_to = "room_images/%Y/%m/%d")
    date_uploaded = models.DateTimeField(auto_now_add = True)
    room = models.ForeignKey(Room, on_delete = models.CASCADE)
    user_uploaded = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.room) + " Photo"

    def  image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="60" height="60" />' % (self.image))

    image_tag.allow_tags = True

class Payment(models.Model):
    payment_date = models.DateTimeField(auto_now_add = True)
    guest = models.ForeignKey(Guest, on_delete = models.CASCADE)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        db_table = "payment" 

class Transaction(models.Model):
    payment = models.ForeignKey(Payment, on_delete = models.CASCADE)
    transaction_name = models.CharField(max_length = 100)
    guest = models.ForeignKey(Guest, on_delete = models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    transaction_amount = models.DecimalField(decimal_places = 2, max_digits = 12)
