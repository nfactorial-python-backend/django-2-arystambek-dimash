from django import forms
from .models import News


class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=150, label="Title")
    description = forms.CharField(max_length=250,required=False)
    content = forms.CharField(widget=forms.Textarea, label="News Description")

    class Meta:
        model = News
        fields = ["title", "description", "content"]

