# Generated by Django 2.2.1 on 2019-11-08 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Article', '0005_auto_20191108_2209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='picture',
        ),
    ]