from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
# Create your views here.


class PostListView(ListView):
    queryset = Post.objects.filter(status='PB')
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blolg/post/list.html'

def post_list(request):
    post_list = Post.objects.filter(status='PB')
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blolg/post/list.html', {'posts': posts})




def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day) 
    return render(request, 'blolg/post/detail.html',{'post': post})
