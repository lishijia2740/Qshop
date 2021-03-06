# Generated by Django 2.2.1 on 2019-11-28 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0004_goods_goods_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(verbose_name='地址')),
                ('phone', models.CharField(max_length=11, verbose_name='收货人手机号')),
                ('name', models.CharField(max_length=32, verbose_name='收货人名字')),
                ('status', models.IntegerField(verbose_name='状态')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.LoginUser')),
            ],
        ),
    ]
