# Generated by Django 3.0.1 on 2020-02-05 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turniket', '0014_auto_20200131_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='modalnumdash',
            field=models.CharField(max_length=50, null=True),
        ),
    ]