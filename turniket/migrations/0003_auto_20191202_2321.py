# Generated by Django 2.2.1 on 2019-12-02 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turniket', '0002_auto_20191202_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='excel',
            name='dat',
            field=models.CharField(default='  ', max_length=30),
        ),
        migrations.AddField(
            model_name='excel',
            name='name',
            field=models.CharField(default='  ', max_length=30),
        ),
        migrations.AddField(
            model_name='excel',
            name='time',
            field=models.CharField(default='  ', max_length=30),
        ),
        migrations.AlterField(
            model_name='excel',
            name='action',
            field=models.CharField(default='  ', max_length=30),
        ),
    ]
