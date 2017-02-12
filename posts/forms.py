from django import forms

from django_summernote.widgets import SummernoteWidget
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
        'content' : SummernoteWidget(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
        'content': forms.Textarea(attrs={'rows' : 2,
                                   'cols' : 88,
                                   'style': 'resize:none;',
                                   },)
        }
        labels = {
        'content': ''
        }
