# Generated by Django 2.2.6 on 2019-10-19 20:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import user_profile.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', imagekit.models.fields.ProcessedImageField(blank=True, default='default.png', null=True, upload_to=user_profile.models.user_directory_path)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('is_subscribed', models.BooleanField(default=True)),
                ('is_sound_on', models.BooleanField(default=True)),
                ('is_google_calendar', models.BooleanField(default=False)),
                ('is_password_set', models.BooleanField(default=False)),
                ('is_profile_set', models.BooleanField(default=False)),
                ('followed_users', models.ManyToManyField(blank=True, default=None, related_name='followed_user', to=settings.AUTH_USER_MODEL, verbose_name='Followed users')),
                ('followers', models.ManyToManyField(blank=True, default=None, related_name='followers', to=settings.AUTH_USER_MODEL, verbose_name='Followers')),
                ('subscribed_tags', models.ManyToManyField(blank=True, default=None, related_name='subscribed_tags', to='post.Tags', verbose_name='Subscribed Tags')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
