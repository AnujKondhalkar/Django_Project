from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    # django convenstions
    # This 'class (Post)'' will be imported from .model of user app
    model = Post
    # django naming --> convenstions <app>/<model>_<viewtype>.html >>> blog/home.html
    template_name = 'blog/home.html'
    # in html home.html page this variable 'posts will be delivered'
    context_object_name = 'posts'
    ordering = ['-date_posted']        # '-' for newest post first


class PostDetailView(DetailView):
    model = Post


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
