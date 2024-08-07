from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
# Create your views here.


class PostListView(ListView):
    queryset = Post.published.all
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blolg/post/list.html'


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            html_message = render_to_string("blolg/email.html", {
                "post": post,
                "post_url": post_url,
                "name": cd['name'],
                "comments": cd['comments']
            })
            # plain_message = strip_tags(html_message)
            # message = EmailMultiAlternatives(
            #     subject = my_subject,
            #     body= plain_message,
            #     from_email= 'ivan123reactions@gmail.com' ,
            #     to= [cd['to']]
            # )
            # message.attach_alternative(html_message, "text/html")
            # message.send()
            send_mail(subject, message, 'ivan123reactions@gmail.com', [cd['to']], html_message=html_message)
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blolg/post/share.html', {'post': post, 'form': form})
#    return render_to_response('blolg/email.html', {'massage': massage})


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blolg/post/list.html', {'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in = post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blolg/post/detail.html',{'post': post, 'comments': comments, 'form': form})#, 'similar_posts': similar_posts})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
    id=post_id,
    status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return render(request, 'blolg/post/comment.html',
    {'post': post, 'form': form, 'comment': comment})