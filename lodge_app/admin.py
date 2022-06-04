from django.contrib import admin
from .models import *

lodge_name = ""
try:
    lodge = lodge.objects.first()
    lodge_name = lodge.name
except:
    pass

admin.site.site_header  =  lodge_name +" Administration"
admin.site.site_title  =  admin.site.site_header
admin.site.index_title  =  admin.site.site_header


# Register your models here.


class BlogAdminArea(admin.AdminSite):
    try:
        lodge = Lodge.objects.first()
        if lodge is not None:
            site_header = lodge.name
        else:
            site_header = "Lodge Admin"
    except:
        site_header =  "Admin"

blog_site = BlogAdminArea(name = 'BlogAdmin')


@admin.register(Amenity)
class AmeniteAdmin(admin.ModelAdmin):
    list_display = ("name", "faIcon",)
    search_fields = ("name",)
    list_filter = ("name",)
    ordering = ("-name",)

from django.contrib.admin.widgets import AdminFileWidget
class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)

            output.append(
                f' <a href="{image_url}" target="_blank">'
                f'  <img src="{image_url}" alt="{file_name}" width="150" height="150" '
                f'style="object-fit: cover;"/> </a>')

        output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))
        return mark_safe(u''.join(output))

#Either stacked or Tabular
class PoliciesAdminInLine(admin.StackedInline):
    model = Policy

class RoomPhotoAdminInline(admin.StackedInline):
    model = RoomPhoto
    #list_display = ("image_tag",)
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    extra = 0


class RerservedRoomInline(admin.StackedInline):
    model = ReservedRoom
    #list_display = ("image_tag",)
    #formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}
    extra = 0


@admin.register(Lodge)
class LodgeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    list_filter = ("name", "description")
    search_fields = ("name",)

    #list_select_related = ('Lodge',)

    #inlines = (PoliciesAdminInLine,)

    def has_add_permission(self, request):
        # if there's already an entry, do not allow adding
        return not Lodge.objects.exists()

@admin.register(Policy)
class PoliciesAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title","lodge")



@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone", "updated_at", "address", "member_since")
    list_filter  = ("first_name", "last_name", "phone", "updated_at", "address", "member_since")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("date_in", "date_out","active","staff_activated","guest","rejected")
    inlines = [RerservedRoomInline]


@admin.register(ReservedRoom)
class ReservedRoomAdmin(admin.ModelAdmin):
    list_display = (
        "reservation","room","created_at","updated_at"
    )

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("number","name","price","updated_at",)
    list_filter = ("number","name","price","updated_at")
    inlines = [RoomPhotoAdminInline,]


@admin.register(RoomPhoto)
class RoomPhotoAdmin(admin.ModelAdmin):
    list_display = ("image_tag","user_uploaded","date_uploaded",)
    readonly_fields = ("image_tag",)


@admin.register(Freebie)
class FreebiesAdmin(admin.ModelAdmin):

    def view_link(self):
        return "<a href='view/%d/'>View</a>"
    view_link.short_description = ''
    view_link.allow_tags = True

    def lodge_name(self, obj):
        return obj.lodge.name


@admin.register(LodgePhoto)
class LodgePhotAdmin(admin.ModelAdmin):
    list_display = ("image_tag", "lodgename")
    readonly_fields = ("image_tag",)
    radio_fields = {"category" : admin.HORIZONTAL}
    list_per_page = 2
    save_on_top = True

    def lodgename(self, obj):
        return obj.lodge.name

@admin.register(LodgeLocation)
class LodgeLocationAdmin(admin.ModelAdmin):
    list_display = ("location_name", "latitude","longitude", "nearbyLocation")
    list_filter = ("location_name",)
    search_fields = ("location_name",)
