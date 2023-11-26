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
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sender')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_receiver')
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender_user} sent {self.body[0:20]} to {self.receiver_user}" # type: ignore
    
    class Meta:
        ordering = ('-date',)

    def save(self, *args, **kwargs):
        self.date = datetime.datetime.now()
        super(Chat, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('chat:chat_detail', kwargs={"pk": self.pk})
    
    def get_all_messages(sender, receiver): # type: ignore
        messages = []
        # get messages between the two users, sort them by date(reverse) and add them to the list
        message1 = Chat.objects.filter(sender_id=sender, recipient_id=receiver).order_by('-date') # get messages from sender to recipient
        for x in range(len(message1)):
            messages.append(message1[x])
        message2 = Chat.objects.filter(sender_id=receiver, recipient_id=sender).order_by('-date') # get messages from recipient to sender
        for x in range(len(message2)):
            messages.append(message2[x])

        # because the function is called when viewing the chat, we'll return all messages as read
        for x in range(len(messages)):
            messages[x].is_read = True
        # sort the messages by date
        messages.sort(key=lambda x: x.date, reverse=False)
        return messages
    
    def get_message_list(u): # type: ignore
        # get all the messages
        m = []  # stores all messages sorted by latest first
        j = []  # stores all usernames from the messages above after removing duplicates
        k = []  # stores the latest message from the sorted usernames above
        for message in Chat.objects.all():
            for_you = message.receiver_user == u  # messages received by the user
            from_you = message.sender_user == u  # messages sent by the user
            if for_you or from_you:
                m.append(message)
                m.sort(key=lambda x: x.sender_user.username)  # sort the messages by senders
                m.sort(key=lambda x: x.date, reverse=True)  # sort the messages by date

        # remove duplicates usernames and get single message(latest message) per username(other user) (between you and other user)
        for i in m:
            if i.sender_user.username not in j or i.receiver_user.username not in j:
                j.append(i.sender_user.username)
                j.append(i.receiver_user.username)
                k.append(i)
        return k

class Image(models.Model):
   chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_images')
   image = models.ImageField(upload_to=get_message_image, blank=True, null=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])