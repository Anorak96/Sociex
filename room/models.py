from django.db import models
from user.models import User
from django.urls import reverse

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    mods = models.ManyToManyField(User, related_name='group_admins', blank=True)
    members = models.ManyToManyField(User, related_name='group_members', blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('room:group', kwargs={"pk": self.pk})
        
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="message_user")
    room = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="message_room")
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.body[0:50]