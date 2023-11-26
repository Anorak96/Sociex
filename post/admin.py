from django.contrib import admin
from .models import Post, Comment, Image

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3

class imageInline(admin.TabularInline):
    model = Image
    extra = 3

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at', 'post_view')
    list_per_page = 20
    list_filter = ('user', 'created_at',)
    search_fields = ('user', 'caption',)
    fieldsets = (
        (None, {'fields': ('user', 'caption', 'likes', 'post_view')}),
    )
    filter_horizontal = ()
    readonly_fields = ['created_at',]
    inlines = [CommentInline, imageInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment','user', 'post', 'created_at')
    list_filter = ('post', 'user',)
    fieldsets = (
        (None, {'fields': ('user', 'post', 'comment')}),
    )
    readonly_fields = ('created_at',)

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'image_tag', 'image')
    list_filter = ('post',)