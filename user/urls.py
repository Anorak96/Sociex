from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),

    path('<pk>/', views.UserDetailView.as_view(), name='profile'),
    path('follow/<pk>', views.FollowView.as_view(), name='follow'),
    path('<pk>/update/', views.UserUpdateView.as_view(), name='update'),
    path('<pk>/following/', views.FollowingView.as_view(), name='following'),
    path('<pk>/follower/', views.FollowerView.as_view(), name='follower'),

]