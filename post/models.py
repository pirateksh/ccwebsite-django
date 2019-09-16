from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
# Create your models here.

# Model manager
# https://www.youtube.com/watch?v=BrbaKmyTOMc&list=PLEsfXFp6DpzQFqfCur9CJ4QnKQTVXUsRy&index=36


class PostManager(models.Manager):
    """
        Overriding all() model manager.
    """
    def all(self, native_user=None, draft=False, *args, **kwargs):
        if native_user is None:
            # All posts
            if not draft:
                return super(PostManager, self).filter(draft=False).filter(post_on_date__lte=timezone.now()).order_by(
                    '-published')
            # Post is draft
            return super(PostManager, self).filter(draft=True).filter(post_on_date__lte=timezone.now()).order_by(
                    '-published')
        else:
            # Posts whose author is native_user
            if not draft:
                return super(PostManager, self).filter(draft=False).filter(post_on_date__lte=timezone.now()).filter(
                    author=native_user).order_by('-published')
            # Post is draft
            return super(PostManager, self).filter(draft=True).filter(post_on_date__lte=timezone.now()).filter(
                    author=native_user).order_by('-published')


class Tags(models.Model):
    name = models.CharField(max_length=255, verbose_name='Tag Name')
    description = models.TextField(blank=True, null=True, verbose_name='Tag Description')

    def __str__(self):
        return self.name


class Post(models.Model):
    # Title of post
    title = models.CharField(max_length=255, blank=False, null=True, verbose_name='Post Title')

    # Content of post
    post_content = RichTextUploadingField(blank=False, null=True, verbose_name='Post Content')

    # Author of post - User model is foreign key
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True
    )

    # Whether pinned to top or Not
    is_pinned = models.BooleanField(default=False)
    is_scheduled = models.BooleanField(default=False)
    # To create Draft and publish post on specific day.
    draft = models.BooleanField(default=False)
    post_on_date = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now())

    # For AJAX likes
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')

    # Date/Time at which post is published
    published = models.DateTimeField(default=datetime.now, blank=True)
    updated = models.DateTimeField(default=datetime.now, blank=True)

    # Tags related to post.
    tags = models.ManyToManyField(Tags, verbose_name='Post Tags', blank=True)
    slug = models.SlugField(default='', blank=True)

    # Is verified or not
    verify_status = models.IntegerField(default=-1, verbose_name='Is verified')

    # Soft delete
    deleted = models.BooleanField(default=False)

    # Whether post is scheduled or not
    is_scheduled = models.BooleanField(default=False)

    # Initialising post manager
    objects = PostManager()

    def save(self, *args, **kwargs):

        """
            Overriding save() method to auto fill slug field of post.

            Note: Without *args and **kwargs, following error was encountered:
            TypeError: save() got an unexpected keyword argument 'force_insert'
        """

        self.slug = slugify(self.title + str(self.pk))
        super(Post, self).save()

    # URL of link to like post using post's slug
    def get_like_url(self):
        return reverse("like_toggle", (), {'slug', self.slug})

    def __str__(self):
        return '%s' % self.title

    @property
    def get_content_type(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return content_type
