from pyexpat import model
from rest_framework.serializers import ModelSerializer
from post.models import Post, Comment, Tag, Image

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'caption', 'tags', 'likes', 'created_at', 'post_view']