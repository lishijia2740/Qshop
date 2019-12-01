from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from Seller.models import *
from Buyer.models import *
# Create your views here.
import hashlib
from django.views.decorators.cache import cache_page
import logging
collect = logging.getLogger("django")


# 密码加密
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


# 主页装饰器
def LoginValid(func):
    def inner(request, *args, **kwargs):
        username = request.COOKIES.get('username')

        user_id = request.COOKIES.get("user_id")
        username_session = request.session.get('username')
        cookie_username = request.COOKIES.get('username')
        if username and username_session and username == username_session:
            flag = LoginUser.objects.filter(username=cookie_username, id=user_id, user_type=1).exists()
            if flag:
                return func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/buyer/login/')
        else:
            return HttpResponseRedirect('/buyer/login')
    return inner


# 主页
@cache_page(120)
def index(request):
    print(request.COOKIES.get('username'))
    goods_type = GoodsType.objects.all()
    types = []
    for one in goods_type:
        goods = one.goods_set.order_by("-goods_price")
        if len(goods) > 4:
            goods_all = goods[:4]
            types.append({"type": one, "goods": goods_all})
        elif len(goods)>0 and len(goods)<=4:
            goods_all = goods
            types.append({"type": one, "goods": goods_all})
    return render(request, 'buyer/index.html', locals())


# 注册
def register(request):
    """
    完成注册功能
    :param request: 请求方式post
    :return:
    """
    email = request.POST.get('email')
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    repassword = request.POST.get('cpwd')
    # 判空
    if email and password and repassword:
        if password == repassword:
            flag = LoginUser.objects.filter(email=email).exists()
            if flag:
                result = '邮箱已被注册！'
            else:
                LoginUser.objects.create(email=email, username=username, password=setPassword(password),user_type=1)
                result = '注册成功！'
        else:
            result = '两次输入的密码不一致！'
    else:
        result = '不能为空！'
    return render(request, 'buyer/register.html', locals())


# 登录
def login(request):
    if request.method == "POST":
        password = request.POST.get('pwd')
        username = request.POST.get('username')
        if password and username:
            user = LoginUser.objects.filter(username=username, password=setPassword(password), user_type=1).first()
            if user:
                # 登录成功跳转index，添加cookie和session
                response = HttpResponseRedirect('/buyer/index/')
                response.set_cookie("username", user.username)
                response.set_cookie("user_id", user.id)
                request.session["username"] = username
                collect.debug("%s is login" % user.username)
                return response
            else:
                result = '账户或者密码不正确'
                return render(request, 'buyer/login.html', locals())

        else:
            result = '账户或密码不能为空！'
            return render(request, 'buyer/login.html', locals())

    return render(request, 'buyer/login.html', locals())


@LoginValid
# 退出
def logout(request):
    response = HttpResponseRedirect('/buyer/login/')
    response.delete_cookie('username')
    response.delete_cookie('user_id')
    del request.session
    return response


#商品列表
def goodslist(request):
    req_type = request.GET.get("req_type")
    keywords = request.GET.get("keywords")
    if req_type == "findall":
        goods_type = GoodsType.objects.get(id=int(keywords))
        goods_all = goods_type.goods_set.all()
        print(goods_all)
    else:
        goods_all = Goods.objects.filter(goods_name__icontains=keywords).all()
        print(goods_all)
    goods_new = goods_all.order_by("-goods_pro_time")[:2]
    return render(request, 'buyer/goods_list.html', locals())


#商品详情
def details(request, goods_id):
    goods = Goods.objects.get(id=int(goods_id))
    address = UserAddress.objects.filter(status=1).first()
    print(address)
    return render(request, 'buyer/detail.html', locals())

@LoginValid
def cart(request):
    user_id = request.COOKIES.get("user_id")
    #按时间逆查找内容

    order_number = PayOrder.objects.filter(order_user=LoginUser.objects.get(id=user_id), order_status=1).values("order_number")
    cart = Cart.objects.filter(Q(payorder__in=order_number) | Q(payorder='0')).all().order_by("-id")
    return render(request, 'buyer/cart.html', locals())


@LoginValid
def person_info(request):
    return render(request, 'buyer/person_info.html', locals())


import time
@LoginValid
def place_order(request):
    ## 生成订单
    ## 获取 商品id
    ## 获取 商品购买数量
    ## 保存订单
    print(request.GET)
    user_id = request.COOKIES.get("user_id")
    goods_id = request.GET.get("goods_id")
    goods_count = request.GET.get("goods_count")
    address_id = request.GET.get("address_id")
    print(address_id)
    goods = Goods.objects.get(id=int(goods_id))
    ## 保存数据
    ## 保存订单
    payorder = PayOrder()
    payorder.order_number = str(time.time()).replace(".", "")
    payorder.order_status = 1  ## 未支付
    payorder.order_total = goods.goods_price * int(goods_count)
    payorder.order_user = LoginUser.objects.get(id=int(user_id))
    payorder.order_address_id = address_id
    payorder.save()
    ## 保存订单详情

    orderinfo = OrderInfo()
    orderinfo.order_id = payorder
    orderinfo.goods = goods
    orderinfo.goods_price = goods.goods_price
    orderinfo.goods_count = int(goods_count)
    orderinfo.goods_total_price = goods.goods_price * int(goods_count)
    orderinfo.store_id = goods.goods_store_id
    orderinfo.save()

    address = UserAddress.objects.get(id=address_id)
    print(address)
    return render(request, "buyer/place_order.html", locals())


@LoginValid
def user_center_order(request):
    ##返回登录用户订单
    user_id = request.COOKIES.get("user_id")
    payorder = PayOrder.objects.filter(order_user=LoginUser.objects.get(id=user_id)).all().order_by("order_status")
    return render(request, 'buyer/user_center_order.html', locals())


@LoginValid
def user_center_site(request):
    user_id = request.COOKIES.get("user_id")
    user = LoginUser.objects.get(id=user_id)
    if request.method == "POST":
        data = request.POST
        useraddress = UserAddress()
        useraddress.user = user
        useraddress.address = data.get("address")
        useraddress.phone = data.get("phone")
        useraddress.name = data.get("name")
        useraddress.status = 0
        useraddress.save()

    user_address_all = UserAddress.objects.filter(user=user).all()

    return render(request, 'buyer/user_center_site.html', locals())


def updateAddress(request):
    if request.method == "POST":
        print(request.POST)
        address_id = request.POST.get("address")
        print(address_id)
        ## 完成修改地址状态
        ## 2. 修改之前选中的地址状态
        user_address = UserAddress.objects.filter(status=1).first()
        user_address.status = 0
        user_address.save()

        ## 1. 修改选中的地址的状态
        user_address = UserAddress.objects.filter(id=address_id).first()
        user_address.status = 1
        user_address.save()

        return HttpResponseRedirect("/buyer/user_center_site/")


from Qshop.settings import alipay


#订单支付
def payorderAli(request):
    order_id = request.GET.get("order_id")
    payorder = PayOrder.objects.get(id=order_id)
    order_string = alipay.api_alipay_trade_page_pay(
        subject='生鲜交易',
        out_trade_no=payorder.order_number,
        total_amount=str(payorder.order_total),
        return_url="http://127.0.0.1:8000/buyer/payresult/",
        notify_url=None
    )
    result = "https://openapi.alipaydev.com/gateway.do?" + order_string
    return HttpResponseRedirect(result)

#支付结果
def payresult(request):
    out_trade_no = request.GET.get("out_trade_no")
    payorder = PayOrder.objects.get(order_number=out_trade_no)
    payorder.order_status = 2
    payorder.save()

    payorder.orderinfo_set.all().update(order_status=2)
    return render(request, 'buyer/payresult.html', locals())


#添加购物车
@LoginValid
def add_cart(request):
    goods_id = request.POST.get("goods_id")
    count = request.POST.get("count", 1)
    user_id = request.COOKIES.get("user_id")
    goods = Goods.objects.get(id=goods_id)
    user = LoginUser.objects.get(id=user_id)
    #保存
    has_cart = Cart.objects.filter(goods=goods, cart_user=user, payorder = '0').first()
    if has_cart:  ##已经有
        has_cart.goods_number += int(count)
        has_cart.goods_total += int(count) * goods.goods_price
        has_cart.save()
    else:
    ## 没有 ## 保存
        cart = Cart()
        cart.goods = goods
        cart.goods_number = int(count)
        cart.cart_user = LoginUser.objects.get(id=user_id)
        cart.goods_total = int(count) * goods.goods_price
        cart.save()
    return JsonResponse({"code": 10000, "msg": "添加购物车成功"})


def place_order_more(request):
    #生成订单
    #获取 购物车id
    user_id = request.COOKIES.get("user_id")
    data = request.POST
    data = data.items()
    res = []
    for key, value in data:
        if key.startswith("cartid"):
            res.append(value)
    user = LoginUser.objects.get(id=user_id)

    #生成订单  2件  1笔订单  2笔订单详情
    if len(res) != 0:
        payorder = PayOrder()
        payorder.order_number = str(time.time()).replace(".", "")
        payorder.order_status = 1
        payorder.order_total = 0
        payorder.order_user = user
        payorder.save()

        order_total = 0
        order_count = 0
        #订单详情
        for c_id in res:    #c_id  购物车id
            cart = Cart.objects.get(id=c_id)
            goods = cart.goods
            orderinfo = OrderInfo()
            orderinfo.order_id = payorder
            orderinfo.goods = goods
            orderinfo.goods_price = goods.goods_price
            orderinfo.goods_count = cart.goods_number
            orderinfo.goods_total_price = cart.goods_total
            orderinfo.store_id = goods.goods_store_id
            orderinfo.save()


            order_total += cart.goods_total
            order_count += cart.goods_number

            cart.payorder = payorder.order_number
            cart.save()

        payorder.order_total = order_total
        payorder.save()

    return render(request, "buyer/place_order.html", locals())


#购物车删除功能
def delete_cart(request):
    cart_id = request.GET.get("cart_id")
    Cart.objects.filter(id=cart_id).delete()
    return HttpResponseRedirect('/buyer/cart/')


#修改购物车数量
def change_cart(request):
    result = {"code": 10001, "msg": ""}
    cart_id = request.GET.get("cart_id")
    type = request.GET.get("type")
    cart = Cart.objects.filter(id=cart_id).first()
    if type == 'add':
        cart.goods_number += 1
        cart.goods_total += cart.goods.goods_price
    else:
        cart.goods_number -= 1
        cart.goods_total -= cart.goods.goods_price
    try:
        cart.save()
        data = {
            "goods_number": cart.goods_number,
            "goods_total": cart.goods_total,
        }
        result = {"code": 10000, "msg": "保存成功", "data": data}
    except:
        result = {"code": 10001, "msg": "保存失败"}

    return JsonResponse(result)


from django.core.cache import cache


def get_goods(request):
    goods_id = request.GET.get("id")
    data = cache.get(goods_id)
    if data:
        print("第一次")
        return HttpResponse(data)
    else:
        print("第二次")
        goods = Goods.objects.get(id=goods_id)
        cache.set(goods_id, goods.goods_name, 600)
        return HttpResponse(goods.goods_name)


def update_goods(request):
    goods_id = request.GET.get("id")
    goods_name = request.GET.get("goods_name")
    goods = Goods.objects.get(id=goods_id)
    data = cache.get(goods_id)
    if data:
        print("第三次")
        cache.delete(goods_id)
    goods.goods_name = goods_name
    goods.save()
    return HttpResponse("保存数据完成")


def myadd(request):
    return render(request, 'buyer/myadddemo.html', locals())


from sdk.sendDD import senddingding
import random
def get_code(request):
    result = {"code":10000,"msg":""}
    ### 发送请求 获取验证码
    """(content = "",isAtAll= True/False,"atMobiles": [])"""
    ### 随机四位数字
    code = random.randint(1000,9999)
    params = {"content": "您的验证码为%s,打死不要告诉别人!!!" % code, "atMobiles": [], "isAtAll": True}
    try:
        senddingding(params)
        ### 保存验证码
        validcode.objects.create(code=code, user=request.GET.get("e mail"))
        result = {"code": 10000, "msg": "发送验证码成功"}

    except:
        result = {"code": 10001, "msg": "发送验证码失败"}
    print(result)
    return JsonResponse(result)