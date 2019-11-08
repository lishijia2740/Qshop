from django.http import HttpResponse
from django.shortcuts import render
from Article.models import *
from django.core.paginator import Paginator

def index(request):
    #最新的六条数据
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

