# Generated by Django 3.0.1 on 2019-12-30 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turniket', '0010_auto_20191229_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='late_camebin',
            field=models.IntegerField(null=True),
        ),
    ]