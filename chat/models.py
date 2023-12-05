from mailbox import Message
from django.db import models
import os
from django.core.validators import FileExtensionValidator
from uuid import uuid4
import datetime
from django.urls import reverse
from user.models import User
from django.db.models import Max

def get_message_image(instance, filename):
    upload_to = '{}/{}/{}_{}'.format('message', instance.chat.sender_user, 'to', instance.chat.receiver_user)
    ext = filename.split('.')[-1]
    filename = '{}_{}_{}_{}.{}'.format(instance.chat.sender_user, 'to', instance.chat.receiver_user, uuid4().hex, ext)
    return os.path.join(upload_to, filename)

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sender')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_receiver')
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender_user} sent {self.body[0:20]} to {self.receiver_user}" # type: ignore

    class Meta:
        ordering = ('-date',)

    def get_absolute_url(self):
        return reverse('chat:chat_detail', kwargs={"pk": self.pk})

    def sender_message(from_user, to_user, body):
        sender_message = Chat(
            user=from_user, 
            from_user=from_user, 
            receiver_user=to_user,
            body=body,
            read=True
        )
        sender_message.save()

        receiver_message = Chat(
            user=to_user,
            sender_user=from_user,
            receiver_user=from_user,
            body=body,
            read=True
        )
        receiver_message.save()

        return sender_message

    def get_message(user):
        users = []
        messages = Chat.objects.filter(user=user).values('receiver_user').annotate(last=Max("date")).order_by("-last")
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['receiver_user']),
                'last': message['last'],
                'unread': Chat.objects.filter(user=user, receiver_user__pk=message['receiver_user'], read=False).count()
            })
        return users
    
class Image(models.Model):
   chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_images')
   image = models.ImageField(upload_to=get_message_image, blank=True, null=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])