# Generated by Django 2.2.1 on 2019-11-28 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0006_orderinfo_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='order_status',
            field=models.IntegerField(choices=[(1, '未支付'), (2, '已支付'), (3, '待发货'), (4, '已发货'), (5, '完成'), (6, '拒收')], default='1', verbose_name='订单详情状态'),
        ),
    ]
