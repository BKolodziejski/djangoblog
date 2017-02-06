from django.shortcuts import render, redirect
from allauth.account.views import SignupView, LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import ProfileForm

class MySignupView(SignupView):
    template_name = 'accounts/signup.html'

class MyLoginView(LoginView):
    template_name = 'accounts/login.html'

class MyLogoutView(LogoutView):
    template_name = 'accounts/logout.html'

@login_required
def profile_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    return render(request, 'accounts/profile.html', { 'profile': profile, })

@login_required
def profile_edit(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    form = ProfileForm(request.POST or None, request.FILES or None,
                       instance=profile)
    if form.is_valid():
        form.save()
        return redirect('accounts:profile')

    return render(request, 'accounts/profile_edit.html', { 'form': form, })
