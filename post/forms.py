from django.forms import ModelForm, forms
# from django.contrib.auth.models import User
# from django.contrib import admin
# from ckeditor.widgets import CKEditorWidget
from post.models import Post, Tags
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from multiselectfield import MultiSelectField


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'post_content', 'tags']
        # widgets = {
        #     'content': CKEditorUploadingWidget(attrs={
        #         'id': 'post-text',
        #         'required': True,
        #         'placeholder': "What's on your mind..."
        #     }),
        # }
