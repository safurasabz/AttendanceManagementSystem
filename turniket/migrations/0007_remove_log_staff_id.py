# Generated by Django 2.2.1 on 2019-12-13 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turniket', '0006_auto_20191213_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='staff_id',
        ),
    ]
