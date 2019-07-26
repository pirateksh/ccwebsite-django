from django import forms
from .models import Comment


class CommentForm(forms.Form):
    # content_type = forms.CharField(widget=forms.HiddenInput)
    # object_id = forms.IntegerField(widget=forms.HiddenInput)
    # parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    comment_text = forms.CharField(label='', widget=forms.Textarea, required=True)

    def clean_content(self):
        comment_text = self.cleaned_data['comment_text']
        if comment_text:
            return comment_text
        raise forms.ValidationError('Please write some comment!')

    class Meta:
        model = Comment
        fields = ('comment_text',)
