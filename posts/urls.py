from django.conf.urls import url
from . import views

app_name = 'posts'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^create/$', views.post_create, name='create'),
    url(r'^search/(?P<text>.+)/', views.search, name='search'),
    url(r'^(?P<pk>[0-9]+)/$', views.post_detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^(?P<pk>[0-9]+)/comment/$', views.comment_create, name='comment'),
    url(r'^(?P<pk>[0-9]+)/comment/(?P<com_pk>[0-9]+)/edit/$',
        views.comment_edit, name='comment_edit'),
    url(r'^(?P<pk>[0-9]+)/comment/(?P<com_pk>[0-9]+)/delete/$',
        views.comment_delete, name='comment_delete'),
    url(r'^tags/(?P<tag_slug>[-\w]+)/$', views.list_tagged_posts, name='tagged_list'),
]
