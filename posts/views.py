import datetime
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q

from taggit.models import Tag
from guardian.shortcuts import assign_perm

from .models import Post, Comment
from .forms import PostForm, CommentForm
from .utils import paginate

# Create your views here.

POSTS_PER_PAGE = 5

def home(request):
    posts = Post.objects.all().order_by('-pub_date')
    user = request.user

    posts = paginate(posts, request, POSTS_PER_PAGE)

    return render(request, 'posts/home.html', { 'posts': posts, })

@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        form.save_m2m() # required by taggit

        assign_perm('change_delete', request.user, obj=post)
        messages.success(request, 'Post Successfully Created')
        return HttpResponseRedirect(reverse_lazy('posts:detail', args=(post.id, )))
    return render(request, 'posts/create.html', {'form': form, })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    #add_flags(request.user, post)
    return render(request, 'posts/detail.html', {'post': post,
                                                 'comments': comments,
                                                 'comment_form': CommentForm()})

@login_required
def post_edit(request, pk):
    user = request.user
    post = get_object_or_404(Post, pk=pk)

    if (not user.has_perm('change_delete', post)):
        raise PermissionDenied

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:detail', pk)

    return render(request, 'posts/create.html', { 'form': form, })

@login_required
def post_delete(request, pk):
    user = request.user
    post = get_object_or_404(Post, pk=pk)

    if (not user.has_perm('change_delete', post)):
        raise PermissionDenied

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post Successfully Deleted")
        return HttpResponseRedirect(reverse_lazy('profile_view', request.user.username))
    else:
        return HttpResponse()

@login_required
def comment_create(request, pk):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = Comment.objects.create(user=request.user,
                                         post=Post.objects.get(id=pk),
                                         content=form.cleaned_data.get('content'))
        assign_perm('change_delete', request.user, obj=comment)
        return redirect('posts:detail', pk)
    messages.error(request, 'There were some errors in your comment')
    #return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/')

@login_required
def comment_edit(request, pk, com_pk):
    user = request.user
    comment = get_object_or_404(Comment, pk=com_pk)

    if (not user.has_perm('change_delete', comment)):
        raise PermissionDenied

    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'accepted'})
    else:
        return JsonResponse(form.errors)

@login_required
def comment_delete(request, pk, com_pk):
    user = request.user
    comment = get_object_or_404(Comment, pk=com_pk)

    if (not user.has_perm('change_delete', comment)):
        raise PermissionDenied

    if request.method == 'POST':
        comment.delete()
        return JsonResponse({'status': 'accepted'})
    else:
        return JsonResponse({'status': 'rejected',
                             'msg': 'POST request required'})

def search(request, text):
    posts = Post.objects.filter(Q(title__contains=text) | Q(content__contains=text))
    posts = paginate(posts, request, POSTS_PER_PAGE)

    if request.is_ajax():
        return render(request, 'posts/search_ajax.html', {'posts': posts})
    else:
        return render(request, 'posts/home.html', {'posts': posts})

def list_tagged_posts(request, tag_slug):
    tag = get_object_or_404(Tag, name=tag_slug)
    posts = paginate(Post.objects.filter(tags__in=[tag]), request, POSTS_PER_PAGE)

    return render(request, 'posts/home.html', { 'posts': posts, 'tag': tag_slug})
