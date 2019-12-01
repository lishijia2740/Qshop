from django.shortcuts import render
from Seller.models import *
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.views import View
from CeleryTask.tasks import Test
import json
# Create your views here.
from Buyer.models import *
import hashlib
from CeleryTask.tasks import *

# 密码加密
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


# 主页装饰器
def LoginValid(func):
    def inner(request, *args, **kwargs):
        email = request.COOKIES.get('email')
        email_session = request.session.get('email')
        username = request.COOKIES.get("username")
        if email and email_session and email == email_session:
            flag = LoginUser.objects.filter(email=email_session, username=username, user_type=0).exists()
            if flag:
                return func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/seller/login/')
        else:
            return HttpResponseRedirect('/seller/login/')
    return inner


# 主页
from CeleryTask.tasks import Test, sendDingDing
from django.db.models import Sum
import datetime
@LoginValid
def index(request):
    user_id = request.COOKIES.get("user_id")
    user = LoginUser.objects.get(id=user_id)
    # month = datetime.datetime.now().month
    month = 11
    print(user_id)
    print(user)
    print(month)

    #  1. 当月成交订单量
    #  当月成交了多少订单   订单详情多少条
    #  条件： 状态 -》  2 3 4 5
    count_order = OrderInfo.objects.filter(store=user, order_status__in=[2, 3, 4, 5], order_id__order_date__month=month).count()
    print(count_order)

    ## 2. 当月的成交额
    ##当月的销售金额总和
    total_mount_money = 0

    total_mount_money = OrderInfo.objects.filter(store=user, order_status__in=[2, 3, 4, 5], order_id__order_date__month=month).aggregate(Sum("goods_total_price")).get("goods_total_price__sum")
    print(total_mount_money)

    # 3. 销量最高的商品
    # 按照销售数量
    # 最多的商品
    ## 按照商品进行 分组   ->  sum(商品的数量)  goods_id
    ## 查询 数量最多的商品
    data = OrderInfo.objects.values("goods").annotate(Sum("goods_count")).order_by("-goods_count__sum").first().get("goods")
    goods_name = Goods.objects.get(id=data).goods_name

    # 4. 当月成交商品的总量
    # 成交单品数量的总和

    total_goods = OrderInfo.objects.filter(store=user, order_status__in=[2, 3, 4, 5], order_id__order_date__month=month).aggregate(Sum("goods_count")).get("goods_count__sum")
    print(total_goods)

    return render(request, 'seller/index.html', locals())


# 注册
def register(request):
    """
    完成注册功能
    :param request: 请求方式post
    :return:
    """
    email = request.POST.get('email')
    password = request.POST.get('password')
    username = request.POST.get('email')
    repassword = request.POST.get('repassword')
    # 判空
    if request.method=="POST":
        if email and password and repassword:
            if password == repassword:
                flag = LoginUser.objects.filter(email=email).exists()
                if flag:
                    result = '用户已被注册！'
                    return render(request, 'seller/register.html', locals())

                else:
                    LoginUser.objects.create(email=email,username=email, password=setPassword(password), user_type=0)
                    result = '注册成功！'
            else:
                result = '两次输入的密码不一致！'
                return render(request, 'seller/register.html', locals())

        else:
            result = '参数不能为空！'
            return render(request, 'seller/register.html', locals())

    return render(request, 'seller/register.html', locals())


# 登录
def login(request):
    if request.method == "POST":
        password = request.POST.get('password')
        username = request.POST.get('email')
        email = request.POST.get('email')
        if password and email:
            user = LoginUser.objects.filter(email=email, password=setPassword(password), user_type=0).first()
            if user:
                # 登录成功跳转index，添加cookie和session
                response = HttpResponseRedirect('/seller/index/')
                response.set_cookie('email', user.email)
                response.set_cookie('username', user.username)
                response.set_cookie('user_id', user.id)
                request.session["email"] = email
                return response
            else:
                result = '账户或者密码不正确'
                return render(request, 'seller/login.html', locals())

        else:
            result = '账户或密码不能为空！'
            return render(request, 'seller/login.html', locals())

    return render(request, 'seller/login.html', locals())


# 退出
def logout(request):
    response = HttpResponseRedirect('/seller/login/')
    response.delete_cookie('email')
    del request.session
    return response


# 忘记密码
def foget(request):
    return render(request, 'seller/forgot-password.html')


@LoginValid
# 商品列表
def goods_list(request, type, page=1):
    """
    :type -> 0代表商品下架
            1代表商品上架
    :param request:
    :param type:
    :param page:
    :return:
    """
    user_id = request.COOKIES.get("user_id")
    print(user_id)
    user = LoginUser.objects.get(id=int(user_id))
    goods = Goods.objects.filter(goods_status=int(type), goods_store=user.id).order_by("-goods_number")
    print(goods)
    goods_obj = Paginator(goods, 10)
    goods_list = goods_obj.page(page)
    return render(request, 'seller/goods_list.html',locals())


# 商品状态
def goods_status(request, type, id):
    """
    商品id
    操作内容：上架，和下架
    :param request:
    :param type:
    :param id:
    :return:
    """
    print(id)
    print(type)
    goods = Goods.objects.filter(id=int(id)).first()
    if type == 'down':
        goods.goods_status = 0
        goods.save()
    else:
        goods.goods_status = 1
        goods.save()
    url = request.META.get("HTTP_REFERER")  # 获取请求资源
    # print(url)
    return HttpResponseRedirect(url)


#个人中心
@LoginValid
def person_info(request):

    user_id = request.COOKIES.get("user_id")
    print(user_id)
    user = LoginUser.objects.get(id=user_id)
    if request.method == "POST":
        data = request.POST
    ## 更新数据
        user.username = data.get("username")
        user.phone_number = data.get("phone_number")
        user.age = data.get("age")
        user.gender = data.get("gender")
        user.address = data.get("address")
        # user.photo = data.get("photo")
        if request.FILES.get("photo"):
            user.photo = request.FILES.get("photo")
        user.save()
        user = LoginUser.objects.get(id=user_id)
    return render(request, "seller/person_info.html", locals())


#添加商品
@LoginValid
def goods_add(request):
    #获取商品信息
    goods_type = GoodsType.objects.all()
    if request.method=="POST":
        user_id = request.COOKIES.get("user_id")
        data = request.POST
        goods = Goods()
        goods.goods_number = data.get("goods_number")
        goods.goods_name = data.get("goods_name")
        goods.goods_price = data.get("goods_price")
        goods.goods_count = data.get("goods_count")
        goods.goods_location = data.get("goods_location")
        goods.goods_safe_data = data.get("goods_safe_data")
        goods.goods_status = 1
        goods.goods_store_id = user_id
        goods.goods_type_id = int(data.get("goods_type"))
        goods.goods_picture = request.FILES.get("goodsfile")
        goods.save()
    return render(request, 'seller/goodsadd.html', locals())


from sdk.sendDD import senddingding
import random

def get_code(request):
    result = {"code":10000,"msg":''}
    code = random.randint(1000,9999)
    params = {
        "conyent":"您的验证码为%s，嘘！不要告诉别人！" % code,
        "atMobules":[],
        "isAtAll":True
    }
    try:
        sendDingDing(params)
        validcode.objects.create(code=code,user=request.GET.get("email"))
        result = {"code":10000,"msg":"发送验证码成功"}
    except:
        result = {"code": 10001, "msg": "发送验证码失败"}
    return JsonResponse(result)


def middletest(request, data):
    # print("我是 视图")
    # return HttpResponse("middletest")
    def test():
        return HttpResponse("xxxxxxx")
    rep = HttpResponse("middletest")
    rep.render = test
    return rep


def order(request):
    user_id = request.COOKIES.get("user_id")
    status = request.GET.get("status")
    order_info = OrderInfo.objects.filter(store=LoginUser.objects.get(id=user_id), order_status=status)
    print(order_info)
    return render(request, 'seller/order.html', locals())

def change_order(request):
    ## 修改状态
    ## 获取到 order_info 的id
    ## 操作的内容 确认发货 取消订单 修改
    order_id = request.GET.get("order_id")
    type = request.GET.get("type")
    order_info = OrderInfo.objects.get(id=order_id)
    if type == "tx":
        ## 提醒用户支付
        ## 发送邮件或者 发送短息
        ## 发钉钉
        params = {
            "content": "您的订单，请立即付款",
            "atMobiles": [],
            "isAtAll": True
        }
        sendDingDing.delay(params)
    elif type == "qx":
        pass
    elif type == "xg":
        pass
    elif type == "fh":
        order_info.order_status = 4
        order_info.save()
    url = request.META.get("HTTP_REFERER")  ## 获取请求的来源
    return HttpResponseRedirect(url)



