from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap  # new
from .sitemaps import PostSitemap

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls', namespace='user')),
    path('', include('post.urls', namespace='post')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('group/', include('room.urls', namespace='room')),

    path('api/user/', include('user.api.urls', namespace='user_api')),
    path('api/post/', include('post.api.urls', namespace='post_api')),

    path('auth/reset_password/', auth_views.PasswordResetView.as_view(
        template_name='user/password_reset_form.html'), name='password_reset'),
    path('auth/reset_password_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('auth/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='user/password_reset_confirm.html'), name='password_reset_confirm'),
    path('auth/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    path('auth/change_password/', auth_views.PasswordChangeView.as_view(
        template_name='user/change-password.html'), name='password_change'),

    # new path below...
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"posts": PostSitemap}},
    ),

    path('__debug__/', include('debug_toolbar.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)