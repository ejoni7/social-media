from django import forms
from .models import *


class CreatForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['series', 'title', 'description', 'image', ]

class ResponseToTopicForm(forms.ModelForm):
    class Meta:
        model=Response
        fields = ['description','image',]