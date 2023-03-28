from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DeleteView, CreateView, DetailView, UpdateView
from .models import Post, Comment
from django.views import View
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin   
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def moment(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'social/moment.html', context)
@login_required
def get_user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'social/user_profile.html', {"user":user})

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'social/moment.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3

class UserPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'social/post_info.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


    
class PostDetailView(LoginRequiredMixin,View):
    # model = Post
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-date_posted')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            form = CommentForm() # empty it
        
        comments = Comment.objects.filter(post=post).order_by('-date_posted')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }

        return render(request, 'social/post_detail.html', context)
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse('moment-detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
   
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostCreateView(LoginRequiredMixin, CreateView): # only mixin works here, login required doesn't work for class in django!!!
    model = Post
    fields = ['title', 'content', 'image']
    
    def form_valid(self, form): # set current login user to the author of the post instance 
        form.instance.author = self.request.user
        return super().form_valid(form)
    
# class CommentCreateView(LoginRequiredMixin, CreateView): # only mixin works here, login required doesn't work for class in django!!!
#     model = Comment
#     fields = ['username','content', 'time']
    
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']
    
    def form_valid(self, form): 
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

