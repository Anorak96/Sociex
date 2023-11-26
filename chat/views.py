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
    form_class = ChatForm

    # context data for latest message to display
    def get(self, request):
        form = ChatForm()
        user = User.objects.get(pk=self.request.user.pk)  # get your primary key
        messages = Chat.get_message_list(user) # get all messages between you and the other user # type: ignore

        other_users = [] # list of other users

        # getting the other person's name fromthe message list and adding them to a list
        for i in range(len(messages)):
            if messages[i].sender_user != user:
                other_users.append(messages[i].sender_user)
            else:
                other_users.append(messages[i].receiver_user)

        messages_list = messages
        context={
            'ichat' : messages_list,
            'other_users' : other_users,
            'form' : form,
            
        }
        return render(request, self.template_name, context)
    
class ChatMessageView(LoginRequiredMixin, generic.View):
    login_url = 'user:login'
    redirect_field_name = 'redirect_to'
    model = Chat
    template_name = "chat/chat.html"
    form_class = ChatForm

    def get(self, request, pk):
        form = ChatForm()
        uchat = Chat.objects.get(pk=pk)
        user = User.objects.get(pk=self.request.user.pk)  # get your primary key
        messages = Chat.get_message_list(user) # get all messages between you and the other user # type: ignore

        other_users = [] # list of other users

        # getting the other person's name fromthe message list and adding them to a list
        for i in range(len(messages)):
            if messages[i].sender_user != user:
                other_users.append(messages[i].sender_user)
            else:
                other_users.append(messages[i].receiver_user)

        messages_list = messages
        context={
            'ichat' : messages_list,
            'other_users' : other_users,
            'uchat' : uchat,
            'form' : form,
            
        }
        return render(request, self.template_name, context)