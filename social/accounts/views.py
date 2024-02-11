from django.shortcuts import render, redirect, get_object_or_404
from .form import *
from accounts.models import User
from topic.models import Topic
from topic.views import main_log_parameters
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from random import randint
from kavenegar import *
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.forms import UserCreationForm
from sorl.thumbnail import get_thumbnail


# Create your views here.
class Rules(generic.TemplateView):
    template_name = 'accounts/rules.html'


class Ends(generic.TemplateView):
    template_name = 'accounts/ends.html'


def send_sms(request, number, template, message):
    try:
        api = KavenegarAPI(
            '66794E75437974365963452B2F367331586E656E6A37722F4F6F5550584E534F4A48556E6B4D725238334D3D')
        params = {
            'receptor': number,
            'template': template,
            'token': message,
            'type': 'sms',  # sms vs call
        }
        response = api.verify_lookup(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def login_costom(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'accounts/login_costom.html', {'form': form, })
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = authenticate(request, phone=User.objects.get(username=data['phone']).phone,
                                    password=data['password'])
            except:
                user = authenticate(request, phone=data['phone'], password=data['password'])
            if user:
                if not user.is_block:
                    login(request, user)
                    return redirect('topic:main')
                else:
                    messages.warning(request, 'کاربری شما تعلیق شده است')
                    return redirect('accounts:register')
            else:
                messages.warning(request, 'اطلاعات وارد شده صحیح نیست')
                return redirect('accounts:login_costom')
        else:
            messages.warning(request, 'اطلاعات وارد شده صحیح نیست')
            return redirect('accounts:login_costom')


def register(request):
    global random_code, number, reguser
    random_code = randint(1000, 9999)
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form, })
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            number = data['phone']
            if User.objects.filter(phone=number).exists():
                moser = User.objects.get(phone=number)
                if not moser.is_active:
                    reguser = moser
                else:
                    messages.success(request, 'کاربری شما فعال است!')
                    return redirect('accounts:login_costom')
            else:
                reguser = User.objects.create_user(username=data['username'], phone=number,
                                                   password=data['password_2'], email=data['email'])

            messages.success(request, ' برای فعلسازی کاربری لطفا پیامک ارسال شده را برای ما ارسال کنید!')
            send_sms(request, (number,), 'verify', random_code)
            return redirect('accounts:phone_check')
        else:
            messages.warning(request, 'اطلاعات وارد شده صحیح نمیباشند')
            return redirect('accounts:register')


def logout_(request):
    logout(request)
    return redirect('accounts:login_costom')


@login_required(login_url='accounts:login_costom')
def profile(request):
    if request.method == 'GET':
        user_form = UserForm(instance=request.user)
        return render(request, 'accounts/profile.html',
                      {'user_form': user_form, })
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user, )
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'پروفایل با موفقیت ویرایش شد', 'success')
            return redirect('topic:main')
        else:
            messages.warning(request, 'اطلاعات وارد شده صحیح نیست!', 'warning')
            return redirect('accounts:profile')


@login_required(login_url='accounts:login_costom')
def password_check(request):
    if request.method == 'GET':
        form = PasswordChangeForm(request.user)
        return render(request, 'accounts/password_check.html', {'form': form})
    if request.method == 'POST':
        pass_form = PasswordChangeForm(request.user, request.POST)
        if pass_form.is_valid():
            pass_form.save()
            update_session_auth_hash(request, pass_form.user)
            messages.success(request, 'پسورد با موفقیت نغییر کرد ')
            return redirect('topic:main')
        else:
            messages.warning(request, 'تغیرات پسورد ناموفق ')
            return redirect('accounts:profile')


class ForgetPassword(auth_views.PasswordResetView):
    template_name = 'accounts/reset_password.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/link.html'


class ResetDone(auth_views.PasswordResetDoneView):
    template_name = 'accounts/reset_password_done.html'


class ConfirmPassword(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/confirm_password.html'
    success_url = reverse_lazy('accounts:confirm_done')


class ConfirmDone(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/confirm_done.html'


# def phone_check(request):
#     if request.method == 'GET':
#         form = CodeForm()
#         return render(request, 'accounts/phone_check.html', {'form': form})
#     if request.method == 'POST':
#         form = CodeForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             if data['code'] == random_code:
#                 reguser.is_active = True
#                 reguser.save()
#                 messages.success(request, 'حساب کاربری برای شما فعال شد')
#                 return redirect('accounts:login_costom')
#             else:
#                 messages.warning(request, 'اطلاعات وارد شده صحیح نیست')
#                 return redirect('accounts:phone_check')
