from django.db import models
from django.conf import settings
# Create your models here.
class Profile(models.Model):
    user              = models.OneToOneField(settings.AUTH_USER_MODEL)
    short_description = models.CharField(max_length = 150, blank=True)
    full_description  = models.TextField(max_length = 4000, blank=True)
    signature         = models.CharField(max_length = 100, blank=True)
    photo             = models.ImageField(upload_to='users', blank=True)
    date_of_birth     = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username + " profile"

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        else:
            return '/static/images/defphoto.png'
