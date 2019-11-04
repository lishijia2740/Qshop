from django.http import HttpResponse
from django.shortcuts import render,render_to_response
from datetime import datetime
import time
def index1(request):
    name = 'zhangsan'
    age = 18
    hobby = ['cos','basketball','football','computer']
    user = {'name':'李四','age':12,'gender':'男'}
    now_time = datetime.now()
    js = """
    <script>
    alert('111');
    </script>
    """
    return render(request,'demo.html',locals())

def index(request):
    return render(request,'index.html')
def about(request):
    return render(request,'about.html')
def listpic(request):
    return render_to_response('listpic.html')
def newlistpic(request):
    return render(request,'newslistpic.html')
def base(request):
    return render(request,'base.html')