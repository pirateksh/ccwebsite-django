from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
# from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from post import views as post_view
from django.utils.timesince import timesince

# Imported Models
from post.models import Post, Tags
from user_profile.models import UserProfile
from .models import Comment

# Imported Forms
from .forms import CommentForm
from home.forms import UserSignupForm
from post.forms import PostForm

# 3rd Party imports
from notifications.signals import notify
# Create your views here.

HOME = '/'


def add_comment(request, post_id):
    """
        Function to add comments.
        Currently NOT IN USE.
    """
    post = Post.objects.get(id=post_id)
    # initial_data = {
    #     'content_type': post.get_content_type,
    #     'object_id': post.id,
    #
    # }
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            # c_type = form.cleaned_data.get('content_type')
            # content_type = ContentType.objects.get(model=c_type)
            # obj_id = form.cleaned_data.get('object_id')
            # content_data = form.cleaned_data.get('content')
            # new_comment, created = Comment.objects.get_or_create(
            #     user=request.user,
            #     content_type=content_type,
            #     object_id=obj_id,
            #     content=content_data,
            # )
            content_data = comment_form.cleaned_data.get('comment_text')
            parent_obj = None

            try:
                parent_id = int(request.POST['parent_id'])
            except:
                parent_id = None

            # Check if parent_id exists
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() == 1:
                    parent_obj = parent_qs.first()

            new_comment, created = Comment.objects.get_or_create(
                user=request.user,
                post=post,
                comment_text=content_data,
                parent=parent_obj,
            )
            if created:
                messages.success(request, f'Comment posted!')
                if parent_obj is None:
                    return redirect(HOME + '#comment-' + str(post.pk) + '-' + str(new_comment.pk))
                else:
                    return redirect(HOME + '#comment-' + str(post.pk) + '-' + str(parent_obj.pk))
                # return HttpResponseRedirect(new_comment.comment_text.get_absolute_url())
            else:
                messages.error(request, f"Not created!")
                return redirect(HOME)
        # else:
            # messages.error(request, f"Please write some comment!")
            # return redirect(HOME)
    else:
        comment_form = CommentForm()
    form = UserSignupForm()
    add_post_form = PostForm()
    posts = post_view.page_maker(request, Post)
    user_profiles = UserProfile.objects.all()
    tags = Tags.objects.all()
    comments = Comment.objects.all()
    context = {
        'comment_form': comment_form,
        'form': form,
        'addpostform': add_post_form,
        'posts': posts,
        'tags': tags,
        'user_profiles': user_profiles,
        'comments': comments,
    }
    return render(request, 'home/index.html', context)


def ajax_add_comment(request, post_id):
    """
        Function to add comments through AJAX.
        Currently IN USE.
    """
    if request.method == "POST":
        post_pk = request.POST['post_pk']
        parent_pk = request.POST['comment_pk']
        comment_content = request.POST['comment_content']
        parent = None
        post = None
        parent_qs = Comment.objects.filter(pk=parent_pk)
        post_qs = Post.objects.filter(pk=post_pk)

        if parent_qs is not None:
            parent = parent_qs.first()

        if post_qs is not None:
            post = post_qs.first()

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            post=post,
            comment_text=comment_content,
            parent=parent,
        )

        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.avatar:
            avatar_url = user_profile.avatar.url
        else:
            avatar_url = '/static/default-profile-picture.jpg'

        timestamp = new_comment.timestamp

        children_count = new_comment.children().count()

        if children_count == 1:
            count_str = str(children_count) + " Reply |"
        else:
            count_str = str(children_count) + " Replies |"

        # Sending Notificaions
        if created:
            if parent is None:
                notify.send(user_profile, recipient=post.author, verb='commented on your post.', target=post)
            else:
                notify.send(user_profile, recipient=post.author, verb='liked your post.', target=post)



        # comments = Comment.objects.filter(post=post)
        # comment_count = comments.count()
        #
        # replies = Comment.objects.filter(post=post).filter(parent=parent)
        # reply_count = replies.count()
        add_comment_url = reverse('Add Comment', kwargs={'post_id': post_pk})
        user_profile_url = reverse('User Profile', kwargs={'username': request.user.username})

        if created:
            result = "SS"
        else:
            result = "ERR"

        """
            Acronyms:
            SS: Success
            ERR: Error
        """

        response_data = {
            'result': result,
            'avatarURL': avatar_url,
            'userName': request.user.username,
            'timestamp': timesince(timestamp),
            'countStr': count_str,
            'addCommentURL': add_comment_url,
            'userProfileURL': user_profile_url,
            # 'commentCount': comment_count,
            # 'replyCount': reply_count,
        }

        return JsonResponse(response_data)
