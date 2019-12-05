from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from django.http import Http404
from taggit.models import Tag
from itertools import chain


# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, 'entries/home.html', {})


def error_handler(request, *args, **kwargs):
    return render(request, 'entries/error404.html', {})


@login_required
def blog_view(request, *args, **kwargs):
    query = request.GET.get('q')

    if query:
        try:
            tag = get_object_or_404(Tag, slug=query)
            if tag:
                posts = list(chain(
                    Post.objects.filter(author=request.user, title__icontains=query).order_by('-date'),
                    Post.objects.filter(author=request.user, tags=tag).order_by('-date')
                ))
            else:
                posts = Post.objects.filter(author=request.user, title__icontains=query).order_by('-date')
        except Http404:
            posts = Post.objects.filter(author=request.user, title__icontains=query).order_by('-date')
    else:
        posts = Post.objects.filter(author=request.user).order_by('-date')
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    blog_posts = paginator.get_page(page)

    return render(request, 'entries/blog.html', {'blog_posts': blog_posts})


class PostView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'entries/post.html'


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'entries/create_post.html'
    fields = ['title', 'text', 'tags', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeletePostView(LoginRequiredMixin, DeleteView):
    template_name = 'entries/delete_post.html'

    def get_object(self):
        print(self)
        id_ = self.kwargs.get('pk')
        return get_object_or_404(Post, id=id_)

    def get_success_url(self):
        return reverse('blog_view')
