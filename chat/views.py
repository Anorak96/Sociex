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
        loggedin = request.user
        messages = Chat.get_message(user=loggedin)
        active_direct = None
        direct = None

        if messages:
            message = messages[0]
            active_direct = message['user'].pk
            directs = Chat.objects.filter(user=loggedin, receiver_user=message['user'])
            directs.update(read=True)

            for message in messages:
                if message['user'].pk == active_direct:
                    message['unread'] = 0

        context={
            'form': form,
            'active_direct': active_direct,
            'messages': messages,
            'direct': direct,
            'loggedin': loggedin,
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
        loggedin = request.user
        messages = Chat.get_message(user=loggedin)
        active_directs = pk

        directs = []
        direct_send = Chat.objects.filter(user=loggedin, receiver_user__pk=pk)
        direct_send.update(read=True)
        directs.append(direct_send)

        direct_receive = Chat.objects.filter(user=pk, receiver_user__pk=loggedin.pk)
        direct_receive.update(read=True)
        directs.append(direct_receive)

        for message in messages:
            if message['user'].pk == pk:
                message['unread'] = 0

        context={
            'form': form,
            'active_directs': active_directs,
            'messages': messages,
            'directs': directs,
            'loggedin': loggedin,
        }
        return render(request, self.template_name, context)
    
class SendMessage(LoginRequiredMixin, generic.View):

    def post(self, request):
        from_user = request.user