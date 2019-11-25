# Generated by Django 2.2.1 on 2019-11-20 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payorder',
            name='order_status',
            field=models.IntegerField(choices=[(1, '未支付'), (2, '已支付'), (3, '待发货'), (4, '已发货'), (5, '完成'), (6, '拒收')], verbose_name='订单状态'),
        ),
    ]
