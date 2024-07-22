# blog/forms.py

from django import forms
from .models import Post
from django.utils import timezone

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'timeStamp']

    def save(self, commit=True):
        if not self.instance.timeStamp:
            self.instance.timeStamp = timezone.now()
        return super().save(commit=commit)

class BlogSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
