from django.urls import path,re_path
from .views import *
from .views import *

urlpatterns = [
    path('index/', index),
    re_path('^$', index),
    path('login/', login),
    path('register/', register),
    path('logout/', logout),
    path('goodslist/', goodslist),
    path('cart/', cart),
    path('person_info/', person_info),
    path('place_order/', place_order),
    path('place_order_more/', place_order_more),
    path('user_center_order/', user_center_order),
    path('user_center_site/', user_center_site),
    re_path('detail/(?P<goods_id>\d+)/', details),
    path('payorder/', payorderAli),
    path('payresult/', payresult),
    path('add_cart/', add_cart),
    path('delete_cart/', delete_cart),
    path('change_cart/', change_cart)
]