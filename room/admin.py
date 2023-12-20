from django.contrib import admin
from .models import Group, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 3

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'description', 'created_at')
    list_per_page = 20
    list_filter = ('created_at', 'created_by',)
    search_fields = ('name', 'created_by', 'created_at',)
    fieldsets = (
        (None, {'fields': ('name', 'description', 'created_by')}),
        ('Admin', {'fields': ('mods',)}),
        ('Member', {'fields': ('members',)}),
    )
    filter_horizontal = ()
    readonly_fields = ['created_at',]
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'room', 'created_at')
    list_per_page = 20
    list_filter = ('room', 'user')
    search_fields = ('user', 'room', 'created_at',)
    fieldsets = (
        (None, {'fields': ('user', 'body', 'room')}),
    )
    filter_horizontal = ()
    readonly_fields = ['created_at',]