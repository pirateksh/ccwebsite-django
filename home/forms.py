from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserSignupForm(UserCreationForm):

    GROUP_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    choice = forms.ChoiceField(choices=GROUP_CHOICES, widget=forms.RadioSelect, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'choice', 'password1', 'password2',)

    # Unique email address
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email already registered.')
        return email
