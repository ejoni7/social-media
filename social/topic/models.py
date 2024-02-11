
from django.db import models
from accounts.models import *
from django_jalali.db import models as jmodels
from django.urls import reverse
from django.template.defaultfilters import slugify

from django.db.models.signals import post_save


class Series(models.Model):
    name = models.CharField(max_length=40)
    icon = models.CharField(max_length=40)

    def __str__(self):
        return str(self.name)


class FatherTopic(models.Model):
    report = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='topic', blank=True, null=True)
    date = jmodels.jDateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, blank=True, related_name='like_users')
    dislike = models.ManyToManyField(User, blank=True, related_name='dislike_users')
    total_like = models.PositiveIntegerField(default=0)
    total_dislike = models.PositiveIntegerField(default=0)
    block = models.BooleanField(default=False)

    @property
    def total_like(self):
        return self.like.count()

    @property
    def total_dislike(self):
        return self.dislike.count()


class Response(FatherTopic):
    respon = models.ForeignKey('Topic', on_delete=models.CASCADE, blank=True, null=True, related_name='response')

    def __str__(self):
        return self.respon.title


# Create your models here.
class Topic(FatherTopic):
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    title = models.CharField(max_length=70)
    slug_topic = models.SlugField(allow_unicode=True, null=True, blank=True)
    total_responses = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('topic:public_topic', args=[self.id, self.slug_topic])

    def __str__(self):
        return str(self.title)


class SameTopics(models.Model):
    key = models.CharField(max_length=50)
    relateds = models.ManyToManyField(Topic, blank=True)


class View(models.Model):
    ip = models.CharField(max_length=30, blank=True, null=True)
    create = jmodels.jDateTimeField(auto_now_add=True, blank=True, null=True)


class MostReact(models.Model):
    day = jmodels.jDateField(auto_now_add=True)
    topic_title = models.CharField(max_length=70)
    topic_id = models.PositiveIntegerField()
    topic_total_responses = models.PositiveIntegerField(default=0)
    topic_slug = models.SlugField(allow_unicode=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.topic_slug:
            self.topic_slug = slugify(self.topic_title)
        return super().save(*args, **kwargs)


class Rewarded(models.Model):
    day = jmodels.jDateField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.day)

    # @property
    # def total_like(self):
    #     return self.like.count()
    #
    # total_like = models.PositiveIntegerField(default=0)
    # total_dislike = models.PositiveIntegerField(default=0)
    # @property
    # def total_dislike(self):
    #     sus = self.dislike.count()
    #     if sus >= 10:
    #         self.block = True
    #     return sus
