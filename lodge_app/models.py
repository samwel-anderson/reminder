from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
import random


class Amenity(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    faIcon = models.CharField(max_length=50, null=True, blank=True)
    lodge = models.ForeignKey("Lodge", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"
        db_table = "Lodge_amenity"

    def __str__(self):
        return self.name


class Lodge(models.Model):
    description = models.TextField(null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    lodgeRoomInfo = models.TextField(max_length=500, null=False, blank=False)

    class Meta:
        verbose_name = "Lodge"
        db_table = "Lodge"

    def __str__(self):
        return self.name


class Menu(models.Model):
    menu_categories = (
        ("Vegeterian", "Vegiterian menus"),
        ("Non Vegeterian Menu", "Non Vegeterian menus")
    )
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to="menuimages/%Y/%m/%d")
    category = models.CharField(max_length=50, choices=menu_categories)
    lodge = models.ForeignKey("Lodge", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"
        db_table = "Lodge_menu"


class Freebie(models.Model):
    name = models.CharField(max_length=200)
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "freebie"
        verbose_name_plural = "freebies"
        db_table = "Lodge_freebie"

    def __str__(self):
        return self.name


class LodgePhoto(models.Model):
    LODGE_PHOTO_CHOICES = (
        ("BEDROOM", "Bedroom"),
        ("OTHER", "Other"),
        ("BUILDING", "Building"),
        ("LOBBY", "Lobby"),
    )
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    category = models.CharField(blank=False, null=False, choices=
    LODGE_PHOTO_CHOICES, default="BEDROOM", max_length=25)
    image = models.ImageField(null=False, blank=False)

    def image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="60" height="60" />' % (self.image))

    image_tag.allow_tags = True

    class Meta:
        verbose_name = "Lodge Photo"
        verbose_name_plural = "Lodge photos"
        db_table = "Lodge_photo"

    def __str__(self):
        return str(self.category) + str(" Photo of ") + str(self.lodge.name)


class LodgeLocation(models.Model):
    location_name = models.CharField(max_length=200, null=False, blank=False)
    latitude = models.DecimalField(blank=True, null=True, decimal_places=8, max_digits=50)
    longitude = models.DecimalField(blank=True, null=True, decimal_places=8, max_digits=50)
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE, null=True, blank=True)
    nearbyLocation = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Lodge Location"
        verbose_name_plural = "Lodge locations"
        db_table = "Lodge_location"

    def __str__(self):
        return self.location_name


class Policy(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE)

    class Meta:
        db_table = "Lodge_policy"
        verbose_name = "Policy"
        verbose_name_plural = "Policies"

    def __str__(self):
        return self.title


class Reservation(models.Model):
    date_in = models.DateField(null=True)
    date_out = models.DateField(null=True)
    room = models.ForeignKey("Room", on_delete=models.CASCADE, null=True)
    comfirmed = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guest")
    reservation_code = models.CharField(null=True, max_length= 40)
    staff_activated = models.ForeignKey(User, on_delete=models.CASCADE, related_name="staff", null=True)

    def save(self, *args, **kwargs):
        self.reservation_code = random.randint(8000, 9999)
        super(Reservation, self).save(*args, **kwargs)

    class Meta:
        db_table = "Lodge_reservation"

    def __str__(self):
        return "Reservation was done at: " + str(self.date_in) + str(self.date_out) + " " + str(self.comfirmed)


class ReservedRoom(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='reserved_rooms')
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.room.name + str(" is reserved ") + str(self.reservation.comfirmed)

    class Meta:
        verbose_name = "Rerseved Room"
        verbose_name_plural = "Reserved Rooms"
        db_table = "Lodge_reserved_room"


class Guest(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    member_since = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Guest"
        verbose_name_plural = "Guests"
        db_table = "Lodge_guest"

    def __str__(self):
        return self.first_name + " " + str(self.last_name) + " Phone: " + self.phone


class Room(models.Model):
    number = models.IntegerField()
    lodge = models.ForeignKey("Lodge", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    published = models.BooleanField(default=True, null=True)
    booked = models.BooleanField(default=False, null=True)
    thumbnail= models.ImageField(upload_to='rooms_images/%Y/%m/%d/', null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        db_table = "Lodge_room"

    def __str__(self):
        return "Room Number {0} which named: {1}".format(self.number, self.name)

    def get_room_images(self):
        images = []

        if hasattr(self, 'room_images'):
            for i in self.room_images.all():
                image_obj = {
                    'room_name': f"{self.name}",
                    'room_image': f"{i.image.url}"
                }
                images.append(image_obj)

            return images
        return None



class RoomPhoto(models.Model):
    image = models.ImageField(upload_to="room_images/%Y/%m/%d")
    date_uploaded = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room_images')
    user_uploaded = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "Lodge_room_photos"

    def __str__(self):
        return str(self.room) + " Photo"

    def image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="60" height="60" />' % (self.image))

    image_tag.allow_tags = True


class Payment(models.Model):
    payment_date = models.DateTimeField(auto_now_add=True)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        db_table = "payment"


class Transaction(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    transaction_name = models.CharField(max_length=100)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_amount = models.DecimalField(decimal_places=2, max_digits=12)

    class Meta:
        db_table = "Lodge_transaction"
