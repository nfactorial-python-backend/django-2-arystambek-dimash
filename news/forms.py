from django import forms
from .models import News
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=150, label="Title")
    description = forms.CharField(max_length=250,required=False)
    content = forms.CharField(widget=forms.Textarea, label="News Description")

    class Meta:
        model = News
        fields = ["title", "description", "content"]


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email","password1", "password2"]

