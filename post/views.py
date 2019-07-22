from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from home.forms import UserSignupForm
from .models import Post, Tags
from django.core.paginator import Paginator  # EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from django.views.generic import RedirectView
# Create your views here.

NUMBER_OF_POSTS_PER_PAGE = 2
HOME = '/'


def page_maker(request, native_user=None, draft=False):
    post_list = Post.objects.all(native_user=native_user, draft=draft)
    paginator = Paginator(post_list, NUMBER_OF_POSTS_PER_PAGE)
    page = request.GET.get('page')
    return paginator.get_page(page)


@login_required
def add_post(request):
    tags = Tags.objects.all()
    if request.method == 'POST':
        addpostform = PostForm(request.POST)
        if addpostform.is_valid():
            post = addpostform.save(commit=False)  # Why commit=False?
            post.save()
            current_user = request.user
            post.author = current_user
            raw_tags = addpostform.cleaned_data.get('tags')

            for raw_tag in raw_tags:
                if raw_tag in tags:
                    post.tags.add(raw_tag)

            post.save()
            messages.success(request, f"Post Added Successfully!")
            return redirect(HOME)
    else:
        addpostform = PostForm()
    form = UserSignupForm()
    posts = page_maker(request)
    context = {
        'form': form,
        'addpostform': addpostform,
        'posts': posts,
        'tags': tags,
    }
    return render(request, 'home/index.html', context)


class PostLikeToggle(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        print(slug)
        obj = get_object_or_404(Post, slug=slug)
        url_ = HOME + '#like-' + str(obj.pk)
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


class PostLikeAPIToggle(APIView):

    authentication_classes = [authentication.SessionAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get('slug')
        obj = get_object_or_404(Post, slug=slug)
        # url_ = HOME + '#like-' + str(obj.pk)
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
        count = obj.likes.count()
        data = {
            'updated': updated,
            'liked': liked,
            'likescount': count,
        }
        return Response(data)
