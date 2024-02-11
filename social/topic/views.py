from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from jdatetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .form import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import *
from direct.models import *
from django.core.paginator import Paginator
from django.db.models import Max
from django.db.models import Q
from django.views import generic
from direct.views import new_notif

forbidens = {'امام', 'امام زمان', 'صلوات', 'کسکش', 'جنده', 'جنده', 'بیناموس', 'بی ناموس',
             'کیر', 'بیشرف', 'پدر سگ', 'جاکش', 'حرومزاده', 'بیشعور', 'بی شعور', 'انتر'
    , 'پفیوز', 'کثافت', 'ریدم دهن', }


# Create your views here.
@login_required(login_url='accounts:login_costom')
def creat_topic(request):
    if request.method == 'GET':
        form = CreatForm()
        names = Series.objects.values('name', 'icon', )
        return render(request, 'topic/creat_topic.html', {'form': form, 'names': names, })
    if request.method == 'POST':
        form = CreatForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            slug = slugify(data['title'])
            top = Topic(series=data['series'], title=data['title'], description=data['description']
                        , image=data['image'], user_id=request.user.id, slug_topic=slug)
            for item in forbidens:
                if item in top.title or item in top.description:
                    messages.warning(request,
                                     'از بکار بردن کلمات ممنوعه بپرهیزید, تاپیک شما توسط ادمین بررسی و در صورت مورد دار نبودن منتشر خواهد شد!')
                    top.block = True
            top.save()
            if not top.block:
                topel = get_object_or_404(Topic, id=top.id, series=data['series'], title=data['title'])
                id = str(topel.id)
                return redirect('topic:public_topic', id, slug)
        messages.warning(request, 'الاعات وارد شده صحیح نیست')
        return redirect('topic:creat_topic')


@login_required(login_url='accounts:login_costom')
def like_dislike_of_user(request, objs):
    context_liked = []
    context_disliked = []
    for status in objs:
        if status.like.filter(id=request.user.id).exists():
            context_liked.append(status.id)
        if status.dislike.filter(id=request.user.id).exists():
            context_disliked.append(status.id)
    return {'context_liked': context_liked, 'context_disliked': context_disliked, }


def public_topic(request, id, slug_topic):
    if request.method == 'GET':
        form = ResponseToTopicForm()
        topic = get_object_or_404(Topic, id=id, slug_topic=slug_topic, block=False)
        sames = SameTopics.objects.values_list('key', 'relateds')

        for item in sames:
            # return HttpResponse(topic.title)
            if item[0] in topic.title or item[0] in topic.description:
                item[1].add(topic)
        topic.total_responses = topic.response.count()
        topic.save()
        mosted = MostReact.objects.filter(day=date.today()).exists()
        # return  HttpResponse()
        if not mosted:
            MostReact(day=date.today(), topic_title=topic.title, topic_id=topic.id,
                      topic_total_responses=topic.total_responses).save()
        if mosted and topic.date.date() == date.today():
            most = get_object_or_404(MostReact, day=date.today())
            if most.topic_total_responses < topic.total_responses:
                most.topic_total_responses = topic.total_responses
                most.topic_id = topic.id
                most.topic_title = topic.title
                most.topic_slug = slugify(most.topic_title)
                most.save()

        serie = get_object_or_404(Series, id=topic.series.id)
        responses = topic.response.filter(block=False)
        paginator = Paginator(responses, 3)
        page_num = request.GET.get('page')
        if responses.exists():
            responses = paginator.get_page(page_num)
        else:
            responses = None
        context = {'form': form, 'topic': topic, 'page_obj': responses, 'series': serie,
                   'like': 'like', 'dislike': 'dislike', 'where': topic.get_absolute_url(), }
        if request.user.is_authenticated and responses:
            context_response = like_dislike_of_user(request, responses)
            chop = (topic,)
            context_topic = like_dislike_of_user(request, chop)
            context_topic['topic_like'] = context_topic.pop('context_liked')
            context_topic['topic_dislike'] = context_topic.pop('context_disliked')
            context.update(context_response)
            context.update(context_topic)

        return render(request, 'topic/public_topic.html', context)
    if request.method == 'POST':
        res = request.POST.get('res')
        form = ResponseToTopicForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            receive = Response(respon_id=res, user_id=request.user.id, description=data['description'],
                               image=data['image'], )
            for item in forbidens:
                if item in receive.description:
                    messages.warning(request,
                                     'از بکار بردن کلمات ممنوعه بپرهیزید, پاسخ شما توسط ادمین بررسی و در صورت مورد دار نبودن منتشر خواهد شد!')
                    receive.block = True
            receive.save()
            return redirect('topic:public_topic', id, slug_topic)
        messages.warning(request, 'اطلاعات وارد شده صحیح نیست')
        return redirect('topic:public_topic', id, slug_topic)


def main_log_parameters(request, value, sere):
    ip = request.META.get('REMOTE_ADDR')
    if not View.objects.filter(ip__exact=ip).exists():
        sus = View.objects.create(ip=ip)
        sus.save()
    views = View.objects.values_list().count()
    series = Series.objects.all()
    result = Topic.objects
    if value:
        if sere:
            sere = get_object_or_404(Series, name__exact=sere)
            tops = result.filter(title__icontains=value, series__exact=sere.id, block=False).order_by('-date')
        else:
            tops = result.filter(title__icontains=value, block=False).order_by('-date')
    else:
        if sere:
            sere = get_object_or_404(Series, name__exact=sere)
            tops = result.filter(block=False, series__exact=sere.id).order_by('-date')
        else:
            tops = result.filter(block=False, ).order_by('-date')
    paginator = Paginator(tops, 3)
    page_num = request.GET.get('page')
    if tops.exists():
        topics = paginator.get_page(page_num)
    else:
        topics = None
    return {'topics': topics, 'search': value, 'sere': sere, 'views': views, 'series': series, 'where': 'topic/main/', }


# def start_day(request):
#     most = MostReact.objects.filter(day=date.today() - timedelta(days=1))
#     rewarded = Rewarded.objects.filter(day=date.today() - timedelta(days=1))
#     if not rewarded.exists() and most.exists():
#         most_react_of_yesterday = MostReact.objects.get(day=date.today() - timedelta(days=1))
#         topic = get_object_or_404(Topic, id=most_react_of_yesterday.topic_id)
#         user = User.objects.get(id=topic.user.id)
#         user.action += 3
#         user.save()
#         Rewarded(day=date.today() - timedelta(days=1), user_id=topic.user.id).save()


def main(request):
    mosts = MostReact.objects.order_by('-day')[0:5]
    value = request.GET.get('search')
    sere = request.GET.get('sere')
    new = new_notif(request)
    custom = main_log_parameters(request, value, sere)
    custom.update({'mosts': mosts})
    if new:
        custom.update({'new': new})
    return render(request, 'topic/main.html', custom)


@login_required(login_url='accounts:login_costom')
def like(request, id, like_, id_res=None):
    message = ''
    topic = get_object_or_404(Topic, id=id, block=False)
    if id_res:
        topic = get_object_or_404(Response, id=id_res, block=False)
    if like_ == 'like':
        if topic.like.filter(id=request.user.id).exists():
            topic.like.remove(request.user)
            message = 'remove like'
        elif topic.dislike.filter(id=request.user.id).exists():
            message = 'do noting'
        else:
            topic.like.add(request.user)
            message = 'like'
    elif like_ == 'dislike':
        if topic.dislike.filter(id=request.user.id).exists():
            topic.dislike.remove(request.user)
            message = 'remove dislike'
        elif topic.like.filter(id=request.user.id).exists():
            message = 'do noting'
        else:
            topic.dislike.add(request.user)
            message = 'dislike'
        topic.save()
        if topic.total_dislike >= 10:
            topic.delete()
            if not Topic.objects.filter(id=id, block=False).exists():
                messages.warning(request, 'تاپیک حذف شد')
                return redirect('topic:main')
    return HttpResponse(message)


# class UserTopics(LoginRequiredMixin,generic.DetailView):
#     template_name = 'topic/user_topics.html'
#     # pk_url_kwarg = 'pk'
#     model = User
#
#
#     def get_context_data(self, **kwargs):
#         pk = self.kwargs.get('pk')
#         context = super().get_context_data(**kwargs)
#         topics = Topic.objects.filter(user_id=pk, block=False)
#         con = {'topics': topics, 'pk': pk, }
#         context.update(con)
#         return context


def user_topics(request, id):
    if request.method == 'GET':
        tops = Topic.objects.filter(user_id=id, block=False).order_by('-date')
        paginator = Paginator(tops, 3)
        page_num = request.GET.get('page')
        if tops.exists():
            # return HttpResponse(page_num)
            topics = paginator.get_page(page_num)
        else:
            topics = None
        loser = get_object_or_404(User, id=id)
        return render(request, 'topic/user_topics.html',
                      {'page_obj': topics, 'loser': loser, 'where': 'topic/user_topics/' + str(id) + '/', })


@login_required(login_url='accounts:login_costom')
def report(request, id, id_res=None):
    if request.method == 'POST':
        topic = get_object_or_404(Topic, id=id)
        if id_res:
            topic = get_object_or_404(Response, id=id_res)
        if not topic.report:
            topic.report = True
            topic.save()
        return JsonResponse({'mesage': 'ممنون از گزارش شما'})


class MostReacts(generic.ListView):
    template_name = 'topic/most_reacts.html'
    model = MostReact
    paginate_by = 5
    queryset = MostReact.objects.all().order_by("-day")
    extra_context = {'where': 'topic/most_reacts/'}

# login_required(login_url='accounts:login_costom')
# def creat (request):
#      if request.method=='GET':
#           pass
#      if request.method=='POST':
#           pass
