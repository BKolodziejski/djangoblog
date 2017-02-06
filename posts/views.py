import datetime
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Post, Comment
from .forms import PostForm, CommentForm
# Create your views here.

POSTS_PER_PAGE = 5
DATETIME_EPSILON = datetime.timedelta(seconds=1)

def home(request):
    posts = Post.objects.all().order_by('-pub_date')

    paginator = Paginator(posts, POSTS_PER_PAGE)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    for post in posts:
        post.edited = True if post.edit_date - post.pub_date > DATETIME_EPSILON else False

    return render(request, 'posts/home.html', { 'posts': posts, })

@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        Post.objects.create(user=request.user,
                            title=form.cleaned_data.get('title'),
                            content=form.cleaned_data.get('content'))
        messages.success(request, 'Post Successfully Created')
        return HttpResponseRedirect('/')   # TODO: Redirect to created post detail
    return render(request, 'posts/create.html', {'form': form, })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    post.edited = True if post.edit_date - post.pub_date > DATETIME_EPSILON else False
    return render(request, 'posts/detail.html', {'post': post,
                                                 'comments': comments,
                                                 'comment_form': CommentForm()})

@login_required
def comment_create(request, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        Comment.objects.create(user=request.user,
                               post=Post.objects.get(id=post_id),
                               content=form.cleaned_data.get('content'))
        return redirect('posts:detail', post_id)
    messages.error(request, 'There were some errors in your comment')
