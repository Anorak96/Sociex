from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from post.forms import PostForm
from django.contrib import messages
from django.views.generic.edit import FormMixin
from .models import User
from django.http import JsonResponse
from post.models import Post, Image, Comment
from post.forms import ImageForm, PostForm, CommentForm
from room.models import Group, Message
from itertools import chain
from django.db.models import Q

class RegisterView(generic.View):
    template_name = 'user/register.html'

    def get(self, request):
        message = ''
        form = CreateUserForm()
        return render(request, self.template_name, context={'message': message, 'form':form })

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect(request.user.get_absolute_url())

        context = {'form':form,}
        return render(request, self.template_name, context)

class LoginView(generic.View):
    template_name = 'user/login.html'
    redirect_authenticated_user=True
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('post:posts')
        return render(request, self.template_name)
        
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email = email, password = password)
        if user is not None:
            login(request, user)
            next_para = self.request.GET.get('next', 'post:posts')
            return redirect(next_para)
        else:
            messages.info(request, 'Username or Password Incorrect.')
        return render(request, self.template_name)

class LogoutView(generic.View):
    def get(self, request):
        logout(request)
        return redirect('user:login')

class UserDetailView(FormMixin, generic.DetailView):
    model = User
    template_name = "user/timeline.html"
    context_object_name = 'profile'
    form_class = PostForm

    # def get_success_url(self):
    #     pk = self.kwargs['pk']
    #     return reverse("user:profile", kwargs={"pk": pk})
    
    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        pk_ = self.kwargs.get("pk")
        pk = User.objects.get(pk=pk_)
        context['posts'] = Post.objects.filter(user=pk)
        context['form'] = PostForm()
        user = self.request.user.pk
        context['followings'] = pk.get_following().exclude(pk=user)
        context['photos'] = Image.objects.filter(post__user=pk).order_by('post')
        context['users'] = User.objects.get_user_to_follow(pk=user) # type: ignore
        
        users = User.objects.get_user_to_follow(pk=user) # type: ignore
        for user in users:
            other_follow = user.get_following()
            user_follow = self.request.user.get_following() # type: ignore
            friends = []
            for f1 in user_follow:
                for f2 in other_follow:
                    if f1 == f2:
                        mut_user = f1
                        friends.append(mut_user)

        my_profile = User.objects.get(pk=self.request.user.pk)
        profile = get_object_or_404(User, pk=pk_)
        if pk in my_profile.following.all():
            context['button_text'] = 'Unfollow'
        else:
            context['button_text'] = 'Follow'
        return context

    def post(self, request, pk):
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
            return redirect(user.get_absolute_url())
        else:
            print(form.errors)
        imageform = ImageForm()
        context = {'form': form, 'imageform': imageform}
        return render(request, self.template_name, context)
        
    def form_valid(self, form):
        form.save()
        return super(UserDetailView, self).form_valid(form)

class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "user/update.html"
    login_url = 'user:login'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse("user:profile", kwargs={"pk": pk})

    def form_valid(self, form):
        if form.instance.pk == self.request.user.pk:
            form.instance.username = self.request.user.username # type: ignore
            return super().form_valid(form)
        else:
            form.add_error(None, 'Post not yours')
            return super().form_valid(form)

    def test_func(self, **kwargs):
        pk_ = self.kwargs.get("pk")
        user = User.objects.get(pk=pk_)
        return user == self.request.user

class FollowView(LoginRequiredMixin, generic.View):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to' 

    def post(self, request, *args, **kwargs):
        my_profile = User.objects.get(pk=request.user.pk)
        other_profile = get_object_or_404(User, pk=self.kwargs['pk'])

        if my_profile == other_profile:
            messages.info("You can't follow yourself") # type: ignore
        else:
            if other_profile in my_profile.following.all():
                my_profile.following.remove(other_profile)
                other_profile.follower.remove(my_profile)
                is_following = False
            else:
                my_profile.following.add(other_profile)
                other_profile.follower.add(my_profile)
                is_following = True
            return JsonResponse({'is_following': is_following})

class FollowingView(LoginRequiredMixin, generic.View):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'
    template_name = "user/following.html"
    model = User
    context_object_name = 'profiles'

    def get(self, request, pk):
        profiles = User.objects.get(pk=pk)
        followings = profiles.get_following().exclude(pk=request.user.pk)
        following = profiles.get_following()
        users = User.objects.get_user_to_follow(pk=request.user.pk) # type: ignore
        photos= Image.objects.filter(post__user=pk).order_by('post')
        
        context = {
            'followings': followings,
            'following': following,
            'profiles' : profiles,   
            'users' : users,
            'photos' : photos,
        }
        return render(request, self.template_name, context)
    
class FollowerView(LoginRequiredMixin, generic.View):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'
    template_name = "user/follower.html"
    model = User
    context_object_name = 'profiles'

    def get(self, request, pk):
        profiles = User.objects.get(pk=pk)
        followers = profiles.get_follower()
        users = User.objects.get_user_to_follow(pk=request.user.pk) # type: ignore
        photos= Image.objects.filter(post__user=pk).order_by('post')


        context = {
            'followers': followers,
            'profiles' : profiles,   
            'users' : users,
            'photos' : photos,
        }
        return render(request, self.template_name, context)
    
class SearchResultsView(generic.ListView):
    template_name = "main/search_results.html"

    # def get_queryset(self):  # new
    #     query = self.request.GET.get("q")
    #     object_list = User.objects.filter(Q(username__icontains=query))
    #     return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        results = []
        qs = None
        object_list2= Post.objects.filter(Q(caption__icontains=query))
        object_list1 = Group.objects.filter(Q(message_room__icontains=query))
        object_list3 = Message.objects.filter(Q(body__icontains=query))
        
        results.append(object_list2)
        results.append(object_list1)
        results.append(object_list3)
        
        if len(results)>0:
            qs = sorted(chain(*results), reverse=True, key=lambda obj: obj.created_at)
        context['result'] = qs

        return context