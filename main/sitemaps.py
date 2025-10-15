from django.contrib.sitemaps import Sitemap
from .models import Post, News, PhotoAlbum

class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return ['home', 'teachers', 'students', 'gallery', 'news_list', 'posts']

    def location(self, item):
        from django.urls import reverse
        return reverse(item)

class PostSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Post.objects.order_by('-date')

    def lastmod(self, obj):
        return obj.date

class NewsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return News.objects.filter(is_active=True).order_by('-date')

    def lastmod(self, obj):
        return obj.date

class AlbumSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return PhotoAlbum.objects.all()

    def lastmod(self, obj):
        return getattr(obj, 'updated', None) or None
