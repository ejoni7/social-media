from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from sorl.thumbnail import ImageField as ThumbImage
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_jalali.db import models as jmodels


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, phone, username, password, email):
        if not phone:
            raise ValueError('شماره همراه خود را وارد کنید')
        if not email:
            raise ValueError('ایمیل خود را وارد کنید')
        if not username:
            raise ValueError('نام کاربری خود را وارد کنید')
        user = self.model(username=username, phone=phone, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, password, email):
        user = self.create_user(phone, username, password, email)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=25, unique=True)
    phone = models.PositiveIntegerField(unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)  # REMOVE BLANK AND NULL FOR LATER
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False, null=True)
    is_block = models.BooleanField(default=False)
    action = models.PositiveIntegerField(default=0)
    GENDER = [('M', 'مرد'), ('F', 'زن')]
    sex = models.CharField(choices=GENDER, max_length=1, blank=True, null=True)
    image = ThumbImage(upload_to='user', default='1.jpg', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ('username', 'email',)
    objects = UserManager()
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.image.path

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_absolute_url(self):
        return reverse('accounts:profile')
