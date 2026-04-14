from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Post, Comment, Categorie, Message
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PostForm, CategorieForm, CommentForm
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
)


class TrendingView(ListView):
    model = Post
    template_name = 'blog/trending.html'
    context_object_name = 'trend_posts'
    paginate_by = 5

    def get_queryset(self):
        posts = Post.objects.annotate(like_count=Count('liked')).order_by('-like_count')
        return posts

    def get_context_data(self, *args, **kwargs):
        cat_list = Categorie.objects.all()
        reponse = super(TrendingView, self).get_context_data(*args, **kwargs)
        reponse["cat_list"] = cat_list
        return reponse


class CatListView(ListView):
    model = Post
    template_name = 'blog/cat_list.html'
    context_object_name = 'cat_posts'
    paginate_by = 5

    def get_queryset(self):
        cats = get_object_or_404(Categorie, categorie_name=self.kwargs.get('cat'))
        return Post.objects.filter(categorie=cats).order_by('-date_posted')

    def get_context_data(self, *args, **kwargs):
        cat_list = Categorie.objects.all()
        reponse = super(CatListView, self).get_context_data(*args, **kwargs)
        reponse["cat_list"] = cat_list
        return reponse


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        cat_list = Categorie.objects.all()
        reponse = super(PostListView, self).get_context_data(*args, **kwargs)
        reponse["cat_list"] = cat_list
        return reponse

    def get_queryset(self):
        try:
            keyword = self.request.GET['q']
        except:
            keyword = ''
        if (keyword != ''):
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword))
        else:
            object_list = self.model.objects.all()
        return object_list


class ReadListView(ListView):
    model = Post
    template_name = 'blog/read_posts.html'
    context_object_name = 'read_posts'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        cat_list = Categorie.objects.all()
        reponse = super(ReadListView, self).get_context_data(*args, **kwargs)
        reponse["cat_list"] = cat_list
        return reponse

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        cat_list = Categorie.objects.all()
        reponse = super(UserPostListView, self).get_context_data(*args, **kwargs)
        reponse["cat_list"] = cat_list
        return reponse

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        cat_list = Categorie.objects.all()
        reponse = super(PostDetailView, self).get_context_data(*args, **kwargs)
        search = get_object_or_404(Post, id=self.kwargs['pk'])
        like = False
        if search.liked.filter(id=self.request.user.id).exists():
            like = True
        read = False
        if search.read_later.filter(id=self.request.user.id).exists():
            read = True

        reponse["cat_list"] = cat_list
        reponse["like"] = like
        reponse["read"] = read
        return reponse


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def get_context_data(self, *args, **kwargs):
        cat_list = Categorie.objects.all()
        reponse = super(PostCreateView, self).get_context_data(*args, **kwargs)
        reponse["cat_list"] = cat_list
        return reponse

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategorieCreateView(LoginRequiredMixin, CreateView):
    model = Categorie
    form_class = CategorieForm

    def get_context_data(self, *args, **kwargs):
        cat_list = Categorie.objects.all()
        reponse = super(CategorieCreateView, self).get_context_data(*args, **kwargs)
        reponse["cat_list"] = cat_list
        return reponse

    def form_valid(self, form):
        return super().form_valid(form)


class CommentView(CreateView):
    model = Comment
    template_name = 'blog/comment_form.html'
    form_class = CommentForm

    def get_context_data(self, *args, **kwargs):
        cat_list = Categorie.objects.all()
        reponse = super(CommentView, self).get_context_data(*args, **kwargs)
        reponse["cat_list"] = cat_list
        return reponse

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/update_comment.html'

    def get_context_data(self, *args, **kwargs):
        cat_list = Categorie.objects.all()
        reponse = super(CommentUpdateView, self).get_context_data(*args, **kwargs)
        reponse["cat_list"] = cat_list
        return reponse

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs.get('nb'))
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


def delete_comment(request, pk, nb):
    Comment.objects.filter(id=pk).delete()
    return redirect('post_detail', pk=nb)


class ContactView(CreateView):
    model = Message
    template_name = 'blog/contact.html'
    form_class = CommentForm

    def get_context_data(self, *args, **kwargs):
        cat_list = Categorie.objects.all()
        reponse = super(ContactView, self).get_context_data(*args, **kwargs)
        reponse["cat_list"] = cat_list
        return reponse


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/update_post.html'

    def get_context_data(self, *args, **kwargs):
        cat_list = Categorie.objects.all()
        reponse = super(PostUpdateView, self).get_context_data(*args, **kwargs)
        reponse["cat_list"] = cat_list
        return reponse

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def delete_post(request, pk):
    Post.objects.filter(id=pk).delete()
    return redirect('index')


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        user = User.objects.get(id=request.POST.get('user_id'))
        text = request.POST.get('text')
        Comment(author=user, post=post, text=text).save()
        messages.success(request, "Your comment has been added successfully.")
    else:
        return redirect('post_detail', pk=pk)
    return redirect('post_detail', pk=pk)


@login_required
def Read_laterView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('read_id'))
    read = False
    if post.read_later.filter(id=request.user.id).exists():
        post.read_later.remove(request.user)
        read = False
    else:
        post.read_later.add(request.user)
        read = True
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


@login_required
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    like = False
    if post.liked.filter(id=request.user.id).exists():
        post.liked.remove(request.user)
        like = False
    else:
        post.liked.add(request.user)
        like = True
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))


@login_required
def Like2View(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    like = False
    if post.liked.filter(id=request.user.id).exists():
        post.liked.remove(request.user)
        like = False
    else:
        post.liked.add(request.user)
        like = True
    return HttpResponseRedirect(reverse('index'))


def SearchView(request):
    try:
        keyword = request.GET['q']
    except:
        keyword = ''
    if (keyword != ''):
        object_list = Post.objects.filter(
            Q(content__icontains=keyword) | Q(title__icontains=keyword))
        con = object_list.count()
    else:
        object_list = Post.objects.all()
        con = object_list.count()

    context = {

        'posts': object_list,
        'keyword': keyword,
        'con': con

    }

    return render(request, 'blog/search.html', context)
