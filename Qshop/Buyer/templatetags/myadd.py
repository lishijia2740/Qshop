#   1.导包
from django import template
#   2.实例化对象
register = template.Library()

#   3.编写自定义的过滤器
@register.filter(name="hh")
def myadd(a):
    return a + a

@register.filter()
def mymanyadd(a,b):
    return a+b

@register.simple_tag()
def myalladd(a,b,c,d):
    return a+b+c+d

@register.filter()
def getaddress(address_id):
    from Seller.models import UserAddress
    address = UserAddress.objects.get(id=address_id)

    return address.name