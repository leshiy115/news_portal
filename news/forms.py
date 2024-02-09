from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Category


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'category',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")
        if title == text:
            raise ValidationError({
                "text": f"Текст не должен быть таким же как название."
            })
        return cleaned_data





# from news.models import *
# from django import forms
# from news.forms import PostForm

