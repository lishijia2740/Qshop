# Generated by Django 2.2.1 on 2019-11-22 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0003_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='payorder',
            field=models.CharField(default='0', max_length=32, verbose_name='订单表的订单号'),
        ),
    ]
