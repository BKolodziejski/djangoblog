from django.conf.urls import url, include
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', views.MyLoginView.as_view(), name='login'),
    url(r'^signup/$', views.MySignupView.as_view(), name='signup'),
    url(r'^logout/$', views.MyLogoutView.as_view(), name='logout'),
    url(r'^change_password/$', views.MyPasswordChangeView.as_view(),
        name='change_password'),
    url(r'^profile/edit/$', views.profile_edit, name='profile_edit'),
]
