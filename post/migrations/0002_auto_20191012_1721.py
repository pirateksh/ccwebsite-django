# Generated by Django 2.2.6 on 2019-10-12 11:51

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
            field=models.DateField(default=datetime.datetime(2019, 10, 12, 11, 51, 23, 156786, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='postview',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 12, 11, 51, 23, 158391, tzinfo=utc)),
        ),
    ]
