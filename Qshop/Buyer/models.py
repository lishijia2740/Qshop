from django.db import models
from Seller.models import LoginUser, Goods

# Create your models here.
ORDER_STATUS = (
    (1, '未支付'),
    (2, '已支付'),
    (3, '待发货'),
    (4, '已发货'),
    (5, '完成'),
    (6, '拒收'),
)

class PayOrder(models.Model):
    order_number = models.CharField(max_length=32, verbose_name='订单编号')
    order_date = models.DateField(auto_now=True, verbose_name="创建日期")
    order_status = models.IntegerField(choices=ORDER_STATUS, verbose_name="订单状态")
    order_total = models.FloatField(verbose_name="订单总价")
    order_user = models.ForeignKey(to=LoginUser, on_delete=models.CASCADE)
    order_address = models.IntegerField(verbose_name="订单收货地址", default=0)

    class Meta:
        db_table = 'payorder'
        verbose_name = '订单表'

class OrderInfo(models.Model):
    order_id = models.ForeignKey(to=PayOrder, on_delete=models.CASCADE)
    goods = models.ForeignKey(to=Goods, on_delete=models.CASCADE)
    goods_price = models.FloatField(verbose_name='商品单价')
    goods_count = models.IntegerField(verbose_name="订单商品数量")
    goods_total_price = models.FloatField(verbose_name="商品小计")
    store = models.ForeignKey(to=LoginUser, on_delete=models.CASCADE)
    order_status = models.IntegerField(choices=ORDER_STATUS, verbose_name="订单详情状态", default="1")

    class Meta:
        db_table = 'orderinfo'
        verbose_name = "订单详情表"

class Cart(models.Model):
    goods = models.ForeignKey(to=Goods, on_delete=models.CASCADE, verbose_name='商品外键')
    goods_number = models.IntegerField(verbose_name='商品数量')
    cart_user = models.ForeignKey(to=LoginUser, on_delete=models.CASCADE, verbose_name='买家')
    goods_total = models.FloatField(verbose_name='单件商品总价')
    payorder = models.CharField(default="0", verbose_name='订单表的订单号', max_length=32)

    class Meta:
        db_table = 'cart'
        verbose_name = '购物车表'


class validcode(models.Model):
    code = models.CharField(max_length=32, verbose_name='验证码内容')
    user = models.CharField(max_length=32, verbose_name='用户')
    data = models.DateTimeField(auto_now=True, verbose_name='创建时间')


