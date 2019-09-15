from django.forms import ModelForm
from post.models import Post

# 3rd Party imports
# from ckeditor_uploader.widgets import CKEditorUploadingWidget
# from ckeditor.widgets import CKEditorWidget
# from multiselectfield import MultiSelectField


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'post_content', 'tags', 'is_scheduled', 'draft']

        #  Tried Earlier:
        # widgets = {
        #     'content': CKEditorUploadingWidget(attrs={
        #         'id': 'post-text',
        #         'required': True,
        #         'placeholder': "What's on your mind..."
        #     }),
        # }
