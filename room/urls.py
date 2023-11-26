from django.urls import path
from . import views

app_name = 'room'
urlpatterns = [
    path('', views.RoomsView.as_view(), name='groups'),
    path('group/<pk>/', views.RoomDetailView.as_view(), name='group'),
    path('create/', views.GroupCreateView.as_view(), name='create'),
    path('create_message/', views.MessageCreateView.as_view(), name='create_message'),
]