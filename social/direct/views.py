from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from accounts.models import *
from django.contrib import messages
from .form import *
from django.db.models import Q
from django.core.mail import EmailMessage

room = None

def alaki(request):
    user= User.objects.get(id=2)
    return HttpResponse(user)
# Create your views here.
@login_required(login_url='accounts:login_costom')
def direct(request, idu, id_):
    get_object_or_404(User, id=id_, is_block=False)
    get_object_or_404(User, id=idu, is_block=False)
    if request.method == 'GET':
        form = DirectForm()
        if not RoomateU.objects.filter(on=idu, man=id_).values('on', 'man', ).exists() and not RoomateU.objects.filter(
                on=id_, man=idu).values('on', 'man', ).exists():
            pos = RoomateU(on=idu, man=id_)
            pos.save()
        if id_ == request.user.id or idu == request.user.id:
            global roomate
            if RoomateU.objects.filter(on=idu, man=id_).values('on', 'man', ).exists():
                roomate = RoomateU.objects.get(on=idu, man=id_)
            else:
                roomate = RoomateU.objects.get(on=id_, man=idu)
            dir = DirectionU.objects.filter(roomate_id=roomate.id).values('roomate_id', 'he_she_id', 'date').last()
            if dir:
                see = Seen.objects.get(roome_id=roomate.id)
                if dir['he_she_id'] != request.user.id and dir['date'] > see.visit:
                    see.person_id = request.user.id
                    see.save()

            directs = DirectionU.objects.filter(roomate_id=roomate.id).order_by('-date')
            return render(request, 'direct/direct.html', {'directs': directs, 'roomate': roomate, 'form': form, })
        else:
            messages.error(request, 'برای  گفتوگو وارد حساب خود شوید')
            return redirect('topic:main')

    if request.method == 'POST':
        form = DirectForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            pire = DirectionU(message=data['message'], he_she_id=request.user.id, roomate_id=roomate.id)
            pire.save()
        else:
            messages.error(request, 'لطفا فیلد مقابل را پر کنید')
        return redirect('direct:direct', idu, id_)


@login_required(login_url='accounts:login_costom')
def search(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'GET':
        form = SearchForm()
        users = User.objects
        if request.GET.get('search'):
            users = users.filter(username__icontains=request.GET.get('search'), is_active=True, is_block=False).values(
                'id', 'username', )
        else:
            users = users.filter(is_active=True, is_block=False).values('id', 'username', )
        return render(request, 'direct/search.html', {'form': form, 'users': users})
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['search']:
                return redirect('direct:direct', data['search'], request.user.id)
        else:
            return redirect(url)


@login_required(login_url='accounts:login_costom')
def handle_notif(request):
    rooms = RoomateU.objects.filter(Q(on=request.user.id) | Q(man=request.user.id))
    persons = []
    not_seens = []
    for rooj in rooms:
        if not rooj.block:
            if not User.objects.get(id=rooj.on).is_block and not User.objects.get(id=rooj.man).is_block:
                person = User.objects.get(id=rooj.on)
                if person.id == request.user.id:
                    person = User.objects.get(id=rooj.man)
                dir = DirectionU.objects.filter(roomate_id=rooj.id).values('he_she_id', 'date', ).last()
                if dir:
                    see = Seen.objects.get(roome_id=rooj.id)
                    if dir['he_she_id'] != request.user.id and dir['date'] > see.visit:
                        not_seens.append(person)
                persons.append(person)
    return {'persons': persons, 'not_seens': not_seens}


@login_required(login_url='accounts:login_costom')
def new_notif(request):
    custom = handle_notif(request)
    return len(custom['not_seens'])


@login_required(login_url='accounts:login_costom')
def direct_list(request):
    custom = handle_notif(request)
    return render(request, 'direct/direct_list.html', custom)


def block(request, id):
    if request.method == 'POST':
        roos = get_object_or_404(RoomateU, id=id)
        directs = roos.direction.all()
        for dire in directs:
            dire.delete()
        roos.block = True
        roos.save()
        messages.warning(request, 'اتاق گفتوگو بنا به در خواست شما بلاک شد!')
    return redirect('direct:direct_list')


@login_required(login_url='accounts:login_costom')
def create_advertise(request):
    if request.method == 'GET' and request.user.action:
        form = AdvertiseForm()
        return render(request, 'direct/create_advertise.html', {'form': form, })
    if request.method == 'POST':
        form = AdvertiseForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            sus = Advertise(user_id=request.user.id, subject=data['subject'], image=data['image'], text=data['text'])
            request.user.action -= 1
            request.user.save()
            sus.save()
            messages.success(request, 'اگهی شما ایجاد شد ، پس از بررسی ادمین منتشر خواهد شد')
        else:
            messages.error(request, 'اطلاعات وارد شده صحیح نیست')
        return redirect('direct:advertise')
    else:
        return redirect('topic:main')


@login_required(login_url='accounts:login_costom')
# def modify_advertise(request, id):
#     adver = get_object_or_404(Advertise, id=id)
#     if request.method == 'GET' and adver.user_id == request.user.id:
#         form = AdvertiseForm(instance=adver)
#         return render(request, 'direct/create_advertise.html', {'form': form, })
#     if request.method == 'POST':
#         form = AdvertiseForm(request.POST, request.FILES, instance=adver)
#         if form.is_valid():
#             form.save()
#             adver.allowed = False
#             adver.save()
#             messages.success(request, 'اگهی شما ایجاد شد ، پس از بررسی ادمین منتشر خواهد شد')
#         else:
#             messages.error(request, 'اطلاعات وارد شده صحیح نیست')
#         return redirect('direct:advertise')
#     else:
#         return redirect('topic:main')


def advertise(request):
    advs = Advertise.objects.all()
    for adv in advs:
        if adv.exp_date < datetime.now():
            adv.delete()
    advs = Advertise.objects.filter(allowed=True).order_by('-create')
    paginator = Paginator(advs, 2)
    page_num = request.GET.get('page')
    if advs.exists():
        advs = paginator.get_page(page_num)
    else:
        advs = None
    return render(request, 'direct/advertise.html', {'page_obj': advs, 'where': 'direct/advertise/', })


def contact_us(request):
    if request.method == 'GET':
        return render(request, 'direct/contact_us.html')
    if request.method == 'POST':
        sub = request.POST.get('subject')
        email = request.POST.get('email')
        contain = request.POST.get('contain')
        contain += '\n' + 'from : ' + email
        sus = EmailMessage(
            sub,
            contain,
            email,
            ('desprdo.kolbe@gmail.com',),
        )
        sus.send(fail_silently=False)
        messages.success(request, 'درخواست شما با موفقیت ارسال شد')
        return redirect('topic:main')
