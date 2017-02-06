from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^create/$', views.post_create, name='create'),
    url(r'^(?P<pk>[0-9]+)/$', views.post_detail, name='detail'),
    url(r'^(?P<post_id>[0-9]+)/comment/$', views.comment_create, name='comment'),
]
