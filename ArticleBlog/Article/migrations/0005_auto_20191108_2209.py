# Generated by Django 2.2.1 on 2019-11-08 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Article', '0004_auto_20191108_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='picture',
            field=models.ImageField(upload_to='images'),
        ),
    ]