from django.db import models
from django.db.models import Manager
# Create your models here.


class MyUser(Manager):
    def addUser(self, email, password):
        flag = LoginUser.objects.filter(email=email, password=password).exists()
        if not flag:
            user = LoginUser.objects.create(email=email, password=password)
            return user
        else:
            return flag
    def getUser(self):
        email = LoginUser.objects.filter(user_type=1).values("email")
        return email

    def getGoods(self, user_id):
        from Buyer.models import PayOrder,OrderInfo
        goods_name_list = []
        payorder = PayOrder.objects.filter(order_user=LoginUser.objects.get(id="user_id"), order_status=2).all()
        for one in payorder:
            order_info = one.orderinfo_set.all()
            for goods in order_info:
                goods_name = goods.goods.values("goods_name")
                goods_name_list.append(goods_name.goods_name)
        return goods_name_list

GENDER_LIST = (
    (0, '女'),
    (1, '男'),
)


class LoginUser(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.IntegerField(choices=GENDER_LIST, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to="img", default="img/111.jpg")
    user_type = models.IntegerField(verbose_name='用户状态', default=1)    #0 代表卖家 ，1 代表买家
    objects = MyUser()

    class Meta:
        db_table = 'loginuser'


class GoodsType(models.Model):
    type_lebal = models.CharField(max_length=32)
    type_desciption = models.TextField()
    type_picture = models.CharField(max_length=64)

    class Meta:
        db_table = 'goodstype'



class Goods(models.Model):
    goods_number = models.CharField(max_length=32, verbose_name="商品编号")
    goods_name = models.CharField(max_length=32, verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品价格")
    goods_count = models.IntegerField(verbose_name="数量")
    goods_location = models.TextField(verbose_name="生产地")
    goods_safe_data = models.IntegerField(verbose_name="保质期")   ##
    goods_pro_time = models.DateField(auto_now=True,verbose_name="生产日期")  ## 生产日期
    goods_status = models.IntegerField(default=1)   ## 0 代表下架   1 代表上架
    goods_picture = models.ImageField(upload_to='img', default='img/111.jpg')
    goods_type = models.ForeignKey(to=GoodsType, on_delete=models.CASCADE)
    goods_store = models.ForeignKey(to=LoginUser, on_delete=models.CASCADE)
    goods_description = models.TextField(verbose_name='商品描述', default="good!")

    class Meta:
        db_table = "goods"


