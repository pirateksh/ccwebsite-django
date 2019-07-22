# Generated by Django 2.2.3 on 2019-07-21 09:12

import datetime
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0019_auto_20190716_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_on_date',
            field=models.DateField(default=datetime.datetime(2019, 7, 21, 9, 12, 52, 600279, tzinfo=utc)),
        ),
    ]
