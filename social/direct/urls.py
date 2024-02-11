from django.urls import path
from . import views

app_name = 'direct'
urlpatterns = [
    path('<int:idu>/<int:id_>/', views.direct, name='direct'),
    path('search/', views.search, name='search'),
    path('direct_list/', views.direct_list, name='direct_list'),
    path('new_notif/', views.new_notif, name='new_notif'),
    path('block/<int:id>/', views.block, name='block'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('advertise/', views.advertise, name='advertise'),
    path('create_advertise/', views.create_advertise, name='create_advertise'),
    # path('modify_advertise/<int:id>/', views.modify_advertise, name='modify_advertise'),
    path('alaki/',views.alaki,name='alaki'),
]
