from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

import datetime

from taggit.managers import TaggableManager

DATETIME_EPSILON = datetime.timedelta(seconds=1)

# Create your models here.
class Post(models.Model):
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title     = models.CharField(max_length=200)
    content   = models.TextField()
    pub_date  = models.DateTimeField(auto_now_add=True, auto_now=False)
    edit_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    tags      = TaggableManager()

    class Meta:
        permissions = (
            ('change_delete', 'Can change and delete post'),
        )

    def __str__(self):
        return str(self.title)

    @property
    def edited(self):
        return True if self.edit_date - self.pub_date > DATETIME_EPSILON else False

    @property
    def similar_posts(self):
        tag_ids = self.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=tag_ids).exclude(id=self.id)
        similar_posts = similar_posts.annotate(same_tags=models.Count('tags'))\
                        .order_by('-same_tags')[:4]
        return similar_posts

class Comment(models.Model):
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post      = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content   = models.TextField(max_length=400)
    pub_date  = models.DateTimeField(auto_now_add=True, auto_now=False)
    edit_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        permissions = (
            ('change_delete', 'Can change and delete comment'),
        )

    def __str__(self):
        return str(self.content)[:30]
