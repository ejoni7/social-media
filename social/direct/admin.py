from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter
import admin_thumbnails

# Register your models here.
class DirectDalInlines(admin.TabularInline):
    model = DirectionU
    list_display = ['he_she', 'message', 'date', 'roomate', ]
    list_filter = ['he_she', 'roomate', ('date', JDateFieldListFilter), ]


class RoomDalAdmin(admin.ModelAdmin):
    list_display = ['id', 'on', 'man', 'block', ]
    list_editable = ['block', ]
    list_filter = ['on', 'man', 'block', ]
    inlines = [DirectDalInlines, ]


class SeeAdmin(admin.ModelAdmin):
    list_display = ['person', 'visit', 'roome', ]

@admin_thumbnails.thumbnail('image')
class AdvertiseAdmin(admin.ModelAdmin):
    list_display = ['subject','user', 'allowed','image_thumbnail', 'create', ]


admin.site.register(DirectionU)
admin.site.register(Seen, SeeAdmin)
admin.site.register(RoomateU, RoomDalAdmin)
admin.site.register(Advertise, AdvertiseAdmin)
