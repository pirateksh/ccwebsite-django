from django.contrib import admin
from post.models import Post, Tags, PostView
# from .forms import PostForm
# Register your models here.

admin.site.register(Post)
admin.site.register(Tags)
admin.site.register(PostView)
# admin.site.register(PostForm)
