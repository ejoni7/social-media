from django import forms
from .models import *


class DirectForm(forms.ModelForm):
    class Meta:
        model = DirectionU
        fields = ['message', ]

class AdvertiseForm(forms.ModelForm):
    class Meta:
        model=Advertise
        fields=['subject', 'text','image']


class SearchForm(forms.Form):
    search = forms.CharField(max_length=40)
