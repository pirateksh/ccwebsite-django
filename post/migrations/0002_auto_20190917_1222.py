# Generated by Django 2.2.3 on 2019-09-17 06:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_on_date',
            field=models.DateField(default=datetime.datetime(2019, 9, 17, 6, 52, 50, 869095, tzinfo=utc)),
        ),
    ]