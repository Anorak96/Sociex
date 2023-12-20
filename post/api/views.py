from django.core import serializers
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from user.api.serializers import UserSerializer
from itertools import chain
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .serializers import PostSerializer
from post.models import Post, Comment, Image, Tag
from user.models import User

@api_view(['GET'])
def post_json(request):
    qs = Post.objects.all()
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data)

class PostFeed(APIView):

    def get(self, request):
        my_post = Post.objects.filter(user=request.user) # type: ignore
        serializer = PostSerializer(my_post)
        return Response(serializer.data)
    
class PostDetail(APIView):
    """User Detail"""
    serializer_class = PostSerializer
    # pagination_class = PageNumberPagination

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.user == user:
            raise PermissionDenied("You can not delete this user. You must be the Owner")
        return super().delete(request, *args, **kwargs) # type:ignore

    def put(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(Post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)