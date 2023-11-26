from django.urls import path
from . import views

app_name = 'user_api'
urlpatterns = [
    path('', views.UserView.as_view(), name='user'),
    path('<pk>', views.UserDetail.as_view(), name='users'),
    path('user/create/', views.RegistrationApiView.as_view(), name='create_user'),
    path('user/<pk>/update/', views.UpdateUserView.as_view(), name='update_user'),

]