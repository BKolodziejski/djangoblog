from django.dispatch import receiver
from .models import Profile
from allauth.account.signals import user_signed_up

@receiver(user_signed_up)
def create_profile(sender, **kwargs):
    request = kwargs['request']
    user = kwargs['user']

    Profile.objects.create(user=user)
