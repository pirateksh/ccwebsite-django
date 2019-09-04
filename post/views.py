from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator  # EmptyPage, PageNotAnInteger
from django.contrib import messages
# from django.contrib.contenttypes.models import ContentType
# from django.views.generic import RedirectView
from django.utils.timesince import timesince
# from comments.views import add_comment
from datetime import datetime
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Imported Models
from user_profile.models import UserProfile
from .models import Post, Tags
from comments.models import Comment
# from comments.models import Comment

# Imported Forms
from comments.forms import CommentForm
from .forms import PostForm
from home.forms import UserSignupForm


NUMBER_OF_POSTS_PER_PAGE = 5


def page_maker(request, model, native_user=None, draft=False):
    post_list = model.objects.all(native_user=native_user, draft=draft).filter(verify_status=1)
    paginator = Paginator(post_list, NUMBER_OF_POSTS_PER_PAGE)
    page = request.GET.get('page')
    return paginator.get_page(page)


# @login_required
# def add_post(request):
#     tags = Tags.objects.all()
#     if request.method == 'POST':
#         addpostform = PostForm(request.POST)
#         if addpostform.is_valid():
#             post = addpostform.save(commit=False)  # Why commit=False?
#             post.save()
#             post.author = request.user
#             raw_tags = addpostform.cleaned_data.get('tags')
#
#             for raw_tag in raw_tags:
#                 if raw_tag in tags:
#                     post.tags.add(raw_tag)
#             post.save()
#             messages.success(request, f"Success! Check Pending Posts in your profile!")
#             return HttpResponseRedirect(reverse("Index"))
#     else:
#         addpostform = PostForm()
#     form = UserSignupForm()
#     posts = page_maker(request, Post)
#     comment_form = CommentForm()
#     context = {
#         'form': form,
#         'addpostform': addpostform,
#         'posts': posts,
#         'tags': tags,
#         'comment_form': comment_form,
#     }
#     return render(request, 'home/index.html', context)


@login_required
def ajax_add_post(request):
    if request.method == "POST":
        title = request.POST['title']
        tags_str = request.POST['tags']
        tags_str = str(tags_str)
        post_content = request.POST['post_content']
        user = request.user
        user_profile = get_object_or_404(UserProfile, user=user)
        tags_qs = Tags.objects.all()
        post = Post.objects.create(title=title, post_content=post_content, author=user)

        selected_tags = []

        for tag in tags_qs:
            if str(tag) in tags_str:
                post.tags.add(tag)
                selected_tags.append(str(tag))

        post.save()

        # likes = post.likes.count()
        # if likes > 1:
        #     likes_count = str(likes) + ' Like'
        # else:
        #     likes_count = str(likes) + 'Likes'

        # if user_profile.avatar:
        #     avatar_url = user_profile.avatar.url
        # else:
        #     avatar_url = '/static/default-profile-picture.jpg'

        # add_comment_url = reverse(add_comment, kwargs={'post_id': post.pk})
        # like_url = reverse('like_toggle', kwargs={'slug': post.slug})

        response_data = {
            'result': 'Post added successfully!',
            # 'postPk': post.pk,
            # 'postTitle': post.title,
            # 'postContent': post.post_content,
            # 'created': timesince(post.published),
            # 'author': post.author.username,
            # 'selectedTags':  selected_tags,
            # 'avatarURL': avatar_url,
            # 'likes': likes,
            # 'likesCountStr': likes_count,
            # 'addCommentURL': add_comment_url,
            # 'isPinned': post.is_pinned,
            # 'likeURL': like_url,
        }

        return JsonResponse(response_data)


@login_required
def ajax_del_post(request):
    if request.method == "GET":
        coming_from = request.GET['coming_from']
        post_pk = request.GET['post_pk']
        post_qs = Post.objects.filter(pk=post_pk)

        if post_qs is None:
            result = "ERR"
        else:
            post = post_qs.first()
            post.delete()
            result = "SS"

        response_data = {
            'postPK': post_pk,
            'comingFrom': coming_from,
            'result': result,
        }
        return JsonResponse(response_data)
    else:
        return HttpResponseRedirect(reverse("Index"))


@login_required
def ajax_edit_post(request):
    if request.method == "POST":
        pk = request.POST['pk']
        updated_title = request.POST['title']
        tags_str = request.POST['tags']
        updated_content = request.POST['post_content']
        original_post_qs = Post.objects.filter(pk=pk)
        tags_qs = Tags.objects.all()

        selected_tags = []
        updated =datetime.now()

        if original_post_qs is None:
            result = 'ERR'
            like_url = None
        else:
            original_post = original_post_qs.first()
            original_tags_qs = original_post.tags.all()

            for original_tag in original_tags_qs:
                original_post.tags.remove(original_tag)

            for tag in tags_qs:
                if str(tag) in tags_str:
                    original_post.tags.add(tag)
                    selected_tags.append(str(tag))

            original_post.title = updated_title
            original_post.post_content = updated_content
            original_post.updated = datetime.now()
            updated = original_post.updated
            original_post.save()
            result = 'SS'
            like_url = reverse('like_toggle', kwargs={'slug': original_post.slug})

        response_data = {
            'result': result,
            'title': updated_title,
            'content': updated_content,
            'selectedTags': selected_tags,
            'postPK': pk,
            'updated': timesince(updated),
            'likeUrl': like_url,
        }

        return JsonResponse(response_data)


@login_required
def post_like_toggle(request, slug):
    post_qs = Post.objects.filter(slug=slug)
    user = request.user
    count = -1
    pk = -1
    if post_qs is None:
        result = "ERR"

    else:
        post = post_qs.first()
        pk = post.pk
        if user.is_authenticated:
            if user in post.likes.all():
                post.likes.remove(user)
                result = "UNLIKED"
            else:
                post.likes.add(user)
                result = "LIKED"
            count = post.likes.count()
        else:
            result = "UNA"
    """
        ERR - Error
        UNLIKED - Unliked
        LIKED - Liked
        UNA - User not authenticated
    """

    response_data = {
        'result': result,
        'likesCount': count,
        'postPK': pk,
    }

    return JsonResponse(response_data)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    author = post.author
    author_profile = get_object_or_404(UserProfile, user=author)
    user_profiles = UserProfile.objects.all()
    comments = Comment.objects.all()
    comment_form = CommentForm()
    form = UserSignupForm()
    tags = Tags.objects.all()
    context = {
        'post': post,
        'author': author,
        'author_profile': author_profile,
        'comments': comments,
        'comment_form': comment_form,
        'user_profiles': user_profiles,
        'tags': tags,
        'form': form,
    }
    return render(request, 'post/post_detail.html', context)


ADMIN_PROFILE = 'profile/admin/'


@login_required
def approve_post(request, slug):
    if request.user.is_superuser:
        post_qs = Post.objects.filter(slug=slug)
        if post_qs:
            post = post_qs.first()
            author = post.author
            author_profile = UserProfile.objects.get(user=author)
            if post.verify_status == -1:
                post.verify_status = 1
                post.save()
                messages.success(request, f"You have approved a post.")
                if author_profile.is_subscribed:
                    pass
            else:
                messages.error(request, f"Oops! Something went wrong. Try again!")
        else:
            messages.error(request, f"Oops! Something went wrong. Try again!")

        return HttpResponseRedirect(reverse("User Profile", kwargs={'username': request.user.username}))
    else:
        messages.info(request, f"You are not authorised to complete this action!")
    return HttpResponseRedirect(reverse("Index"))


@login_required
def reject_post(request, slug):
    if request.user.is_superuser:
        post_qs = Post.objects.filter(slug=slug)
        if post_qs:
            post = post_qs.first()
            author = post.author
            author_profile = UserProfile.objects.get(user=author)
            if post.verify_status == -1:
                post.verify_status = 0
                post.save()
                messages.success(request, f"You have rejected a post.")
                if author_profile.is_subscribed:
                    pass
            else:
                messages.error(request, f"Oops! Something went wrong. Try again!")
        else:
            messages.error(request, f"Oops! Something went wrong. Try again!")

        return HttpResponseRedirect(reverse("User Profile", kwargs={'username': request.user.username}))
    else:
        messages.info(request, f"You are not authorised to complete this action!")
    return HttpResponseRedirect(reverse("Index"))

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
# from django.contrib.auth.models import User
#
#
# class PostLikeAPIToggle(APIView):
#
#     authentication_classes = [authentication.SessionAuthentication, ]
#     permission_classes = [permissions.IsAuthenticated, ]
#
#     def get(self, request, slug=None, format=None):
#         # slug = self.kwargs.get('slug')
#         obj = get_object_or_404(Post, slug=slug)
#         # url_ = HOME + '#like-' + str(obj.pk)
#         user = self.request.user
#         updated = False
#         liked = False
#         if user.is_authenticated:
#             if user in obj.likes.all():
#                 liked = False
#                 obj.likes.remove(user)
#             else:
#                 liked = True
#                 obj.likes.add(user)
#             updated = True
#         count = obj.likes.count()
#         data = {
#             'updated': updated,
#             'liked': liked,
#             'likescount': count,
#         }
#         return Response(data)
