from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
# Imported Models
from post.models import Post
from .models import Comment

# Imported Forms
from .forms import CommentForm
from home.forms import UserSignupForm
from post.forms import PostForm

# Create your views here.

HOME = '/'


def add_comment(request, post_id):
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
        else:
            messages.error(request, f"Please write some comment!")
            return redirect(HOME)
    else:
        comment_form = CommentForm()
    form = UserSignupForm()
    addpostform = PostForm()
    context = {
        'comment_form': comment_form,
        'form': form,
        'addpostform': addpostform,
    }
    return render(request, 'home/index.html', context)
