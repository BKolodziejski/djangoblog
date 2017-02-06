from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title     = models.CharField(max_length=200)
    content   = models.TextField()
    pub_date  = models.DateTimeField(auto_now_add=True, auto_now=False)
    edit_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.title)

class Comment(models.Model):
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post      = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    content   = models.TextField(max_length=400)
    pub_date  = models.DateTimeField(auto_now_add=True, auto_now=False)
    edit_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.content)[:30]
