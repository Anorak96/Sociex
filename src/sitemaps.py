from django.contrib.sitemaps import Sitemap
from post.models import Post


class PostSitemap(Sitemap):
    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.created_at