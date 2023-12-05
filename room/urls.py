from django.urls import path
from . import views

app_name = 'room'
urlpatterns = [
    path('', views.RoomsView.as_view(), name='groups'),
    path('<pk>/', views.RoomDetailView.as_view(), name='group'),
    path('group/create/', views.GroupCreateView.as_view(), name='create'),
    path('message/', views.MessageCreateView.as_view(), name='create_message'),
    path('group/<pk>/delete/', views.GroupDeleteView.as_view(), name='group_delete'),
    path('group/<pk>/join/', views.GroupJoinView.as_view(), name='group_join'),
    path('group/<pk>/leave/', views.GroupLeaveView.as_view(), name='group_leave'),
    path('group/<pk>/update/', views.GroupUpdateView.as_view(), name='group_update'),
    path('message/<pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),
    path('message/<pk>/update/', views.MessageUpdateView.as_view(), name='message_update'),


    
]