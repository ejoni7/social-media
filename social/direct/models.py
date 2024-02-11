from django.db import models
from accounts.models import *
from django.db.models.signals import post_save
from django_jalali.db import models as jmodels
from jdatetime import datetime
from datetime import timedelta


class Advertise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    allowed = models.BooleanField(default=False)
    subject = models.CharField(max_length=40)
    image = models.ImageField(upload_to='advertise', blank=True, null=True)
    text = models.TextField(max_length=500)
    create = jmodels.jDateTimeField(auto_now_add=True)
    exp_date = jmodels.jDateTimeField(default=datetime.now() + timedelta(days=30))


# Create your models here.
class RoomateU(models.Model):
    block = models.BooleanField(default=False)
    on = models.IntegerField()
    man = models.IntegerField()

    def __str__(self):
        return str(self.id)


class DirectionU(models.Model):
    message = models.TextField(max_length=400)
    date = jmodels.jDateTimeField(auto_now_add=True)
    roomate = models.ForeignKey(RoomateU, on_delete=models.CASCADE,related_name='direction')
    he_she = models.ForeignKey(User, on_delete=models.CASCADE)


class Seen(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    roome = models.OneToOneField(RoomateU, on_delete=models.CASCADE)
    visit = jmodels.jDateTimeField(auto_now=True)


def save_seen(sender, **kwargs):
    if kwargs['created']:
        los = Seen(roome=kwargs['instance'], person_id=kwargs['instance'].man, visit=datetime.now())
        los.save()


post_save.connect(save_seen, sender=RoomateU)
