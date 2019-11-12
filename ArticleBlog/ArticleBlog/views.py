from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from Article.models import *
from django.core.paginator import Paginator
from Article.form import UserForm

def index(request):
    #最新的六条数据
    print(request.COOKIES.get('username'))
    newarticle = Article.objects.order_by("-data")[:6]
    #返回图文推荐  7条数据
    recommendarticle = Article.objects.filter(recommend=1)[:7]
    #点击率
    clickarticle = Article.objects.order_by('-click')[:12]
    return render(request,'index.html',locals())
def about(request):
    return render(request,'about.html')
def listpic(request):
    return render(request,'listpic.html')
def newslistpic(request,page):
    article = Article.objects.all()
    page = int(page)
    #查看数据
    paginator = Paginator(article,6)
    page_obj = paginator.page(page)

    # 获取当前页
    number = page_obj.number
    start = number - 3
    end = number + 2
    if number<=2:
        start=0
        end=5
    if number >=paginator.num_pages -2:
        end = paginator.num_pages
        start = end-5
    page_range = paginator.page_range[start:end]

    return render(request,'newslistpic.html',locals())

def articleDetails(request,id):
    id = int(id)
    article = Article.objects.filter(id=id).first()
    article.click +=1
    article.save()
    return render(request,'articleDetails.html',locals())

def AddArticle(request):
    # author = Author.objects.filter().first()  ## 查询第一条 数据
    # type = Type.objects.filter().first()
    # for i in range(100):
    #     article = Article()
    #     article.title = "title_%s" % i
    #     article.content = "content_%s" % i
    #     article.description = "description_%s" % i
    #     article.author = author
    #     article.save()
    #     article.type.add(type)
    #     article.save()
    return HttpResponse('增加数据！')


#------------
import hashlib
def http(request):
    print(dir(request))
    print(request.COOKIES)
    print(request.method)
    print(request.FILES)
    print(request.GET)
    print(request.GET.get('name'))
    print(request.POST)
    print(request.POST.get('name'))
    print(request.scheme)
    print(request.path)
    print(request.body)
    print(request.META.get('os'))
    print(request.META.get('HTTP_USER_AGENT'))
    print(request.META.get('HTTP_HOST'))
    print(request.META.get('HTTP_REFERER'))
    print(request.META)
    serch_key = request.GET.get('searchkey')
    article=[]
    if serch_key:
        article = Article.objects.filter(title__icontains=serch_key).all().values('title')
    return  render(request,'search.html',locals())

def httppost(request):
    register_form = UserForm()
    if request.method=='POST':
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        data = UserForm(request.POST)
        if data.is_valid():
            clean_data = data.cleaned_data
            username = clean_data.get('name')
            password = clean_data.get('password')
            if username and password:
                flag = User.objects.filter(name=username)
                if not flag:
                    user = User()
                    user.name=username
                    user.pwd =setPassword(password)
                    user.save()
                    result = 'ok!'
                else:
                    result = '账户已存在！'
            else:
                result = '账户或密码为空'
        else:
            result=data.errors
    return render(request,'register.html',locals())

def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

#______________
def ajaxdemo(request):
    return render(request,'ajaxreq.html',locals())

def ajaxreq(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    print(username)
    print(password)
    result = {"code":10000,"msg":""}
    if username and password:
        flag = User.objects.filter(name=username, pwd=setPassword(password)).exists()
        if flag:
            result["msg"]='存在'
        else:
            result["msg"]='不存在'
            result["code"]='10001'
    else:
        result["msg"] = '用户名或者密码为空'
        result["code"] = '10002'
    return JsonResponse(result)


def ajaxnew(request):
    return render(request,'ajaxnew.html',locals())
def ajaxpost(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    result = {"code": 10000, "msg": ""}
    if username and password:
        flag = User.objects.filter(name=username, pwd=setPassword(password)).exists()
        print(flag)
        if flag:
            result["msg"] = '已存在！'
        else:
            User.objects.create(name=username,pwd=setPassword(password))
            result["msg"] = '注册成功！'
            result["code"] = '10001'

    else:
        result["msg"] = '账户或密码为空'
        result["code"] = '10002'
    return JsonResponse(result)

def checkuser(request):
    username = request.GET.get('username')
    if username:
        user = User.objects.filter(name=username).first()
        if user:
            result = {"code":10001,"msg":'账号已存在！'}
        else:
            result = {"code": 10002, "msg": '账号合法！'}
    else:
        result = {"code": 10002, "msg": '参数为空！'}
    return JsonResponse(result)
def login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        result ={'code':10000,'msg':''}
        if username and password:
            user = User.objects.filter(name=username, pwd=setPassword(password))
            if user:
                response = HttpResponseRedirect('/index')
                response.set_cookie('username', username)
                return response
            # else:
            #     return HttpResponseRedirect('/index')
        else:
            return HttpResponse('参数为空！')
    return render(request,'login.html')

def logout(request):
    response = HttpResponseRedirect('/logout')
    response.delete_cookie("username")
    return response