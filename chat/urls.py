from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.ChatView.as_view(), name='chat_index'),
    path('<pk>', views.ChatMessageView.as_view(), name='chat_detail'),
    path('send-message', views.SendMessage.as_view(), name='send_message'),
    
]