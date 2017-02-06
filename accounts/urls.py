from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', views.MyLoginView.as_view(), name='login'),
    url(r'^signup/$', views.MySignupView.as_view(), name='signup'),
    url(r'^logout/$', views.MyLogoutView.as_view(), name='logout'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^profile/edit/$', views.profile_edit, name='profile_edit'),
]