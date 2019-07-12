from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
# Create your models here.


class Tags(models.Model):
    name = models.CharField(max_length=255, verbose_name='Tag Name')
    description = models.TextField(blank=True, null=True, verbose_name='Tag Description')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Post Title')
    content = RichTextUploadingField(blank=True, null=True, verbose_name='Post Content')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True
    )

    published = models.DateTimeField(default=datetime.now, blank=True)
    tags = models.ManyToManyField(Tags, verbose_name='Post Tags', blank=True)
    slug = models.SlugField(default='', blank=True)

    def save(self):
        self.slug = slugify(self.title)
        super(Post, self).save()

    def __str__(self):
        return '%s' % self.title



