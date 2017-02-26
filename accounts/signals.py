from django.dispatch import receiver
from .models import Profile
from allauth.account.signals import user_signed_up
from guardian.shortcuts import assign_perm

@receiver(user_signed_up)
def create_profile(sender, **kwargs):
    request = kwargs['request']
    user = kwargs['user']

    profile = Profile.objects.create(user=user)
    assign_perm('change', user, obj=profile)
