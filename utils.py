from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect

def paginate(objects, request, num_per_page=5):
    paginator = Paginator(objects, num_per_page)

    page = request.GET.get('page')
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        return paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return paginator.page(paginator.num_pages)

def set_theme(request):
    request.session['preferred_theme'] = request.GET.get('theme', 'default') + '.css'
    print("AAA" + request.GET.get('theme', 'default'))
    return redirect('posts:home')
