from django.urls import path
from . import views

app_name = 'post_api'
urlpatterns = [
    path('post_json', views.post_json, name='post_json'),
    path('', views.PostFeed.as_view(), name='post'),
    path('<pk>', views.PostDetail.as_view(), name='posts'),

]