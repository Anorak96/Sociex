from django.contrib import admin
from .models import Post, Comment, Image

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 3

class imageInline(admin.TabularInline):
    model = Image
    extra = 3
    fields = ['image']
    template = 'admin/post/image/tabular.html'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at', 'likes_count', 'post_view')
    list_per_page = 20
    list_filter = ('user', 'created_at',)
    search_fields = ('user', 'caption',)
    fieldsets = (
        (None, {'fields': ('user', 'caption', 'likes', 'post_view')}),
    )
    filter_horizontal = ()
    readonly_fields = ['created_at',]
    inlines = [CommentInline, imageInline]

    def likes_count(self, obj):
        return obj.likes.count()
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment','user', 'post', 'created_at')
    list_filter = ('post', 'user',)
    fieldsets = (
        (None, {'fields': ('user', 'post', 'comment')}),
    )
    readonly_fields = ('created_at',)
    list_per_page = 20

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'image_tag', 'image')
    list_filter = ('post',)
    list_per_page = 10

    # def image(self, obj):
    #     return mark_safe('<img src="{url}" width="{width}" height="{height}"/>'.format (
    #         url = obj.image.url,
    #         width = obj.image.width,
    #         height = obj.image.height,
    #     )
    # )