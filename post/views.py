from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from home.forms import UserSignupForm
from .models import Post, Tags
from django.contrib.auth.models import User
from django.contrib import messages
from home.views import page_maker
# Create your views here.


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
            return redirect('/home/')
        else:
            messages.info(request, f"Form Invalid!")
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
