# Generated by Django 2.2.1 on 2019-11-19 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Seller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_number', models.CharField(max_length=32, verbose_name='商品编号')),
                ('goods_name', models.CharField(max_length=32, verbose_name='商品名称')),
                ('goods_price', models.FloatField(verbose_name='商品价格')),
                ('goods_count', models.IntegerField(verbose_name='数量')),
                ('goods_location', models.TextField(verbose_name='生产地')),
                ('goods_safe_data', models.IntegerField(verbose_name='保质期')),
                ('goods_pro_time', models.DateField(auto_now=True, verbose_name='生产日期')),
                ('goods_status', models.IntegerField(default=1)),
                ('goods_picture', models.ImageField(default='img/111.jpg', upload_to='img')),
                ('goods_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.LoginUser')),
                ('goods_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.GoodsType')),
            ],
            options={
                'db_table': 'goods',
            },
        ),
    ]
