from django.urls import path, re_path
from . import views

app_name = 'topic'
urlpatterns = [
    path('creat_topic/', views.creat_topic, name='creat_topic'),
    path('most_reacts/', views.MostReacts.as_view(), name='most_reacts'),
    re_path(r'public_topic/(?P<id>\d+)/(?P<slug_topic>[-\w]+)/$', views.public_topic, name='public_topic'),
    path('main/', views.main, name='main'),
    path('like/<int:id>/<str:like_>/<int:id_res>/', views.like, name='like'),
    path('like/<int:id>/<str:like_>/', views.like, name='like_topic'),
    # path('dislike/<int:id>/<str:like_>/<int:id_res>/', views.dislike, name='dislike'),
    path('user_topics/<int:id>/', views.user_topics, name='user_topics'),
    path('report/<int:id>/', views.report, name='report_top'),
    path('report/<int:id>/<int:id_res>/', views.report, name='report_rec'),

]