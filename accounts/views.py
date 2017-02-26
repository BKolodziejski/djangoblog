from django.shortcuts import render, redirect, get_object_or_404
from allauth.account.views import SignupView, LoginView, LogoutView,\
                                  PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .models import Profile
from posts.models import Post
from utils import paginate
from .forms import ProfileForm

class MySignupView(SignupView):
    template_name = 'accounts/signup.html'

    def __init__(self):
        super().__init__()
        self.success_url = reverse_lazy('accounts:profile_edit')

class MyLoginView(LoginView):
    template_name = 'accounts/login.html'

class MyLogoutView(LogoutView):
    template_name = 'accounts/logout.html'

class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('posts:home')
    template_name = 'accounts/change_password.html'

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    posts = Post.objects.filter(user=user).order_by('-pub_date')

    posts = paginate(posts, request, 5)

    return render(request, 'accounts/profile.html', { 'profile': profile,
                                                      'posts'  : posts})

@login_required
def profile_edit(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    form = ProfileForm(request.POST or None, request.FILES or None,
                       instance=profile)
    if form.is_valid():
        form.save()
        return redirect('profile', user.username)

    return render(request, 'accounts/profile_edit.html', { 'form': form, })
