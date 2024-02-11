from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as base
from django.contrib.auth.models import Group
from .form import *
import admin_thumbnails


# Register your models here.
@admin_thumbnails.thumbnail('image')
class UserAdmin(base):
    form = UserChangeForm
    add_form = UserCreatForm
    list_display = ('id','username', 'image_thumbnail','is_active','is_block',)
    list_editable = ('is_block',)
    list_filter = ('username', 'is_block',)
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()
    fieldsets = (
        ('user', {'fields': ('username', 'phone','email','image_thumbnail',)}),
        ('status', {'fields': ('is_active', 'is_admin','is_block','action',)})
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'phone', 'password1', 'password2')}),
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'sex', 'image', 'bio', ]


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
