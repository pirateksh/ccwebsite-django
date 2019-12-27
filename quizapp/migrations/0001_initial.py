# Generated by Django 2.2.6 on 2019-10-19 20:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('no_of_ques', models.PositiveIntegerField(default=0)),
                ('max_score', models.PositiveIntegerField(default=0)),
                ('neg_marks', models.PositiveIntegerField(default=0)),
                ('time_lim', models.PositiveIntegerField(help_text='Time Limit should be in MINUTES.')),
                ('instructions', models.TextField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UserQuizResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('is_atm', models.BooleanField(default=0)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.Quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RandomQuizQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_ques_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.Quiz'),
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option1', models.TextField()),
                ('option2', models.TextField()),
                ('option3', models.TextField(blank=True, null=True)),
                ('option4', models.TextField(blank=True, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.Question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.Quiz')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CurrentQuiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sel_ans', models.CharField(max_length=1)),
                ('is_atm', models.BooleanField(default=False)),
                ('contrib', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.Question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.Quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corr_answer', models.CharField(choices=[('1', 'option1'), ('2', 'option2'), ('3', 'option3'), ('4', 'option4')], max_length=1)),
                ('extra_info', models.TextField(blank=True, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.Question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.Quiz')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
