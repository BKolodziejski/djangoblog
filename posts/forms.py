from django import forms

from django_summernote.widgets import SummernoteInplaceWidget
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
        'content' : SummernoteInplaceWidget(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
        'content': forms.Textarea(attrs={'rows'       : 2,
                                         'style'      : 'resize:none; width: 100%',
                                         'placeholder': 'Comment',
                                   },)
        }
        labels = {
        'content': ''
        }
