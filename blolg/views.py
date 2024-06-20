from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post
# Create your views here.



def post_list(request):
    posts = Post.objects.filter(status='PB')
    context = {
        'posts': posts,
    }
    return render(request, 'blolg/post/list.html', context)



def post_detail(request, id):
    post = get_object_or_404(Post,id=id, status=Post.Status.PUBLISHED) 
    return render(request, 'blolg/post/detail.html',{'post': post})
