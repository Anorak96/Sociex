from django.contrib import admin
from .models import Chat, Image

class imageInline(admin.TabularInline):
    model = Image
    extra = 3

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('date', 'body', 'sender_user', 'receiver_user')
    fieldsets = (
        (None, {
            "fields": ('sender_user', 'receiver_user', 'body', 'date', 'read'),
        }),
    )
    list_filter = ('sender_user', 'receiver_user', 'date',)
    readonly_fields = ('date',)
    ordering = ('-date',)
    inlines = [imageInline]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'image')
    list_filter = ('chat',)