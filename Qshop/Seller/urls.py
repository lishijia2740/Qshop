from django.urls import path,re_path
from .views import *
urlpatterns = [
    path('index/',index),
    path('login/',login),
    path('logout/',logout),
    path('register/',register),
    path('foget/', foget),
    path('person_info/',person_info),
    path('goods_list/', goods_list),
    path('goods_list/', goods_list),
    path('goodsadd/', goods_add),
    re_path('goods_list/(?P<type>\d{0,1})/(?P<page>\d+)/', goods_list),
    re_path('goods_status/(?P<type>\w+)/(?P<id>\d+)/', goods_status),
    re_path('middleteest/(?P<date>\w+)/', middletest),
]