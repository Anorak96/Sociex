from django.urls import path
from . import views

urlpatterns = [
    path('comment/<pk>', views.CommentJson.as_view(), name='comment_json'),
    path('post_json', views.post_json, name='post_json'),
    path('post/<pk>/like/', views.LikeView.as_view(), name='like_post'),
]