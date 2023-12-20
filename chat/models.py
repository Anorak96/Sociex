from django.db import models
import os
from django.core.validators import FileExtensionValidator
from uuid import uuid4
from django.urls import reverse
from user.models import User
from django.db.models import Max

def get_message_image(instance, filename):
    upload_to = '{}/{}/{}_{}'.format('message', instance.chat.sender_user, 'to', instance.chat.receiver_user)
    ext = filename.split('.')[-1]
    filename = '{}_{}_{}.{}'.format(instance.chat.sender_user, 'to', instance.chat.receiver_user, ext)
    return os.path.join(upload_to, filename)

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sender')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_receiver')
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date',)

    def get_absolute_url(self):
        return reverse('chat:chat_detail', kwargs={"pk": self.pk})

    def sender_message(self, sender_user, receiver_user, body):
        sender_message = Chat(
            user=sender_user, 
            from_user=sender_user, 
            receiver_user=receiver_user,
            body=body,
            read=True
        )
        sender_message.save()

        receiver_message = Chat(
            user=receiver_user,
            sender_user=sender_user,
            receiver_user=sender_user,
            body=body,
            read=True
        )
        receiver_message.save()

        return sender_message

    def get_message(self, user):
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