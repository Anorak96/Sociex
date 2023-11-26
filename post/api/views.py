from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
import json
from django.core import serializers
from django.http import JsonResponse
from post.forms import ImageForm, PostForm, CommentForm
from post.models import Post, Comment, Image
from user.models import User

def post_json(request):
    qs = Post.objects.all()
    data = serializers.serialize('json', qs)
    return JsonResponse({'data': data})

class CommentJson(LoginRequiredMixin, generic.View):
    model = Comment
    template_name = 'post/detail.html'

    def post(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        pk = self.kwargs.get("pk")
        posts = Post.objects.get(pk=pk)
        data = json.loads(request.body)
        newcomm = data["comment"]
        comment = Comment.objects.create(user=user, post=posts, comment=newcomm)
        return JsonResponse(comment.comment, safe=False)

class LikeView(LoginRequiredMixin, generic.View):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'

    def post(self, request, pk):
        data = json.loads(request.body)
        pk_ = data["pk"]
        post = Post.objects.get(pk=pk_)
        checker = None
        
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            checker = 0
        else:
            post.likes.add(request.user)
            checker = 1
        likes = post.likes.count()
        info = {
            "check": checker,
            "num_of_likes": likes
        }
        return JsonResponse(info, safe=False)