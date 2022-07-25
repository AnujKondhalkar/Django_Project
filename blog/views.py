from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

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
    paginate_by = 5


class UserPostListView(ListView):
    # django convenstions
    # This 'class (Post)'' will be imported from .model of user app
    model = Post
    # django naming --> convenstions <app>/<model>_<viewtype>.html >>> blog/home.html
    template_name = 'blog/user_posts.html'
    # in html home.html page this variable 'posts will be delivered'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        # here post form instance author is assigned current user
        form.instance.author = self.request.user
        return super().form_valid(form)  # validate via parent class using super()


# loginmixin just authenticate user
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        # here post form instance author is assigned current user
        form.instance.author = self.request.user
        return super().form_valid(form)  # validate via parent class using super()

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:  # current user authentication
            return True
        return False


class PostDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:  # current user authentication
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
