from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter


# Register your models here.


class TopicAdmin(admin.ModelAdmin):
    list_display = ['title','id', 'user', 'date', 'block', 'report', 'total_responses', ]
    list_editable = ['block', ]
    search_fields = ['user', 'title', 'id', ]
    prepopulated_fields = {
        'slug_topic': ('title',)
    }
    list_filter = (
        ('date', JDateFieldListFilter), 'block', 'report',
    )


class SeriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', ]


class ViewAdmin(admin.ModelAdmin):
    list_display = ['ip', 'create']

class RewardedAdmin(admin.ModelAdmin):
    list_display = ['user', 'day']

class SameTopicsAdmin(admin.ModelAdmin):
    list_display = ['key',]

class MostReactAdmin(admin.ModelAdmin):
    list_display = ['topic_title', 'day']
    prepopulated_fields = {
        'topic_slug': ('topic_title',)
    }


admin.site.register(Series, SeriesAdmin)
admin.site.register(SameTopics, SameTopicsAdmin)
admin.site.register(Rewarded, RewardedAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(MostReact, MostReactAdmin)
admin.site.register(View, ViewAdmin)
