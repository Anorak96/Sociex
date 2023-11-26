from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .forms import ChatForm, ImageForm
from django.db.models import Max
from django.views import generic
from django.db.models import Q
from user.models import User
from .models import Chat, Image
from django.contrib.auth.mixins import LoginRequiredMixin

class ChatView(LoginRequiredMixin, generic.View):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'
    model = Chat
    template_name = "chat/chat.html"

    def get(self, request):
        user = request.user
        ichat = Chat.objects.filter(Q(sender_user=user) | Q(receiver_user=user)).distinct()
        chat = Chat.objects.all().last()

        chats = Chat.objects.filter(sender_user=user).values('receiver_user').annotate(last=Max('date')).order_by('-last')
        users = []
        for chat in chats:
            users.append({
                'receiver_user': User.objects.get(pk=chat['receiver_user']),
                
                'unread': Chat.objects.filter(sender_user=chat['receiver_user'], receiver_user__pk=user, read=False).count(),
                })
    
        context={
            'ichat' : ichat,
            'users' : users,
            'chat' : chat,
        }
        return render(request, self.template_name, context)
    
class ChatMessageView(LoginRequiredMixin, generic.View):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'
    model = Chat
    template_name = "chat/chat.html"
    form_class = ChatForm

    def get(self, request, pk):
        user = request.user
        ichat = Chat.objects.filter(Q(sender_user=user) | Q(receiver_user=user)).distinct()
        uchat = Chat.objects.get(pk=pk)
        chat = Chat.objects.all().last()

        chats = Chat.objects.filter(sender_user=user).values('receiver_user').annotate(last=Max('date')).order_by('-last')
        users = []
        for chat in chats:
            users.append({
                'receiver_user': User.objects.get(pk=chat['receiver_user']),
                
                'unread': Chat.objects.filter(sender_user=chat['receiver_user'], receiver_user__pk=user, read=False).count(),
                })
    
        context={
            'ichat' : ichat,
            'users' : users,
            'chat' : chat,
            'uchat' : uchat,
        }
        return render(request, self.template_name, context)
    