from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from itertools import chain
from tomlkit import comment
from post.forms import ImageForm, PostForm, CommentForm
from post.models import Post, Comment, Image
from user.models import User
from room.models import Group, Message

class PostListView(LoginRequiredMixin, generic.ListView):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'
    model = Post
    template_name = "post/post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk_ = self.kwargs.get("pk")
        user = User.objects.get(pk=self.request.user.pk) # get object of logged in user
        following = [prof for prof in user.following.all()] # profile that logged in user is folowing
        posts = []
        qs = None
        #=== following posts===
        for us in following:
            u_post = us.user_post.all()
            posts.append(u_post)
        my_post = self.request.user.user_post.all() # type: ignore
        posts.append(my_post)
        #=== sort and chain post query===
        if len(posts)>0:
            qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.created_at)
        context['posts'] = qs
        user = self.request.user.pk
        context['users'] = User.objects.get_user_to_follow(pk=user) # type: ignore
        context['groups'] = Group.objects.all().filter(members=user)

        groups = Group.objects.all().filter(members=user)
        grp_mess = []
        qs_mess = None
        #=== Group message==
        for group in groups:
            u_group = group.message_room.all().exclude(user=user)  # type: ignore
            grp_mess.append(u_group)
        #=== sort and chain messages query===
        if len(grp_mess)>0:
            qs_mess = sorted(chain(*grp_mess), reverse=True, key=lambda obj: obj.created_at)
        context['grp_msgs'] = qs_mess
        
        return context 
    
class PostDetailView(FormMixin, generic.DetailView):
    model = Post
    template_name = "post/detail.html"
    form_class = CommentForm

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse("post:detail", kwargs={"pk": pk})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        pk_ = self.kwargs.get("pk")
        context['post'] = Post.objects.get(pk=pk_)
        post = get_object_or_404(Post, pk=pk_)
        context['comments'] = Comment.objects.filter(post=post)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        user = User.objects.get(pk=request.user.pk)
        pk_ = self.kwargs.get("pk")
        post = Post.objects.get(pk=pk_)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.post = post
            instance.save()
            messages.success(request, "Comment Created.")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(PostDetailView, self).form_valid(form)

class PostCreate(LoginRequiredMixin, generic.View):
    template_name = 'post/create.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        form = PostForm()
        return render(request, self.template_name, context={'form':form })

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        images = request.FILES.getlist("images")
        user = User.objects.get(pk=request.user.pk)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            for i in images:
                image = Image.objects.create(post=instance, image=i)
                image.save()
            post = Post.objects.get(pk=instance.pk)
            return redirect(post.get_absolute_url())
        
        else:
            print(form.errors)
        imageform = ImageForm()
        context = {'form': form, 'imageform': imageform}
        return render(request, self.template_name, context)

class CommentCreate(LoginRequiredMixin, generic.View):
    template_name = 'post/detail.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'
        
    def get(self, request):
        form = CommentForm()
        return render(request, self.template_name, context={'form':form })

    def post(self, request):
        form = CommentForm(request.POST)
        user = User.objects.get(pk=request.user.pk)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.post = Post.objects.get(id=request.POST.get('post_comment'))
            print(request.POST.get('post_comment'))
            instance.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            print(form.errors)
        context = {'form': form}
        return render(request, self.template_name, context)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = 'post/delete.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get_success_url(self) -> str:
        return reverse('post:posts')

    def test_func(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        post = Post.objects.get(pk=pk_)
        return post.user == self.request.user

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = 'post/comm_delete.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)
        com_pos = comment.post
        return reverse('post:detail', kwargs={"pk": com_pos.pk})

    def test_func(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        comment = Comment.objects.get(pk=pk_)
        return comment.user == self.request.user

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post    
    form_class = PostForm
    template_name = 'post/update.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        return reverse('post:detail', kwargs={"pk": pk})

    def form_valid(self, form):
        user = User.objects.get(pk=self.request.user.pk)
        images = self.request.FILES.getlist("images")
        if form.instance.user == user:
            for i in images:
                image = Image.objects.create(post=form.instance, image=i)
                image.save()
            return super().form_valid(form)
        else:
            form.add_error(None, 'Post not yours')
            return super().form_invalid(form)
    
    def test_func(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        post = Post.objects.get(pk=pk_)
        return post.user == self.request.user

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment    
    form_class = CommentForm
    template_name = 'post/comm_update.html'
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)
        com_pos = comment.post
        return reverse('post:detail', kwargs={"pk": com_pos.pk})

    def form_valid(self, form):
        user = User.objects.get(pk=self.request.user.pk)
        if form.instance.user == user:
            return super().form_valid(form)
        else:
            form.add_error(None, 'Comment is  not yours')
            return super().form_invalid(form)
    
    def test_func(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        comment = Comment.objects.get(pk=pk_)
        return comment.user == self.request.user

class LikeView(LoginRequiredMixin, generic.View):

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        user = self.request.user

        if user in post.likes.all():
            post.likes_num -= 1
            post.likes.remove(user)
            is_liked = False
            post.save()
        else:
            post.likes_num += 1
            post.likes.add(user)
            is_liked = True
            post.save()
        return JsonResponse({'likes':post.likes_num, 'isliked': is_liked})

        
