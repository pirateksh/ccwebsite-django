from django import forms
from .models import Comment


class CommentForm(forms.Form):
    # content_type = forms.CharField(widget=forms.HiddenInput)
    # object_id = forms.IntegerField(widget=forms.HiddenInput)
    # parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea, required=True)

    def clean_content(self):
        content = self.cleaned_data['content']
        if content:
            return content
        raise forms.ValidationError('Please write some comment!')

    class Meta:
        model = Comment
        fields = ('content',)
