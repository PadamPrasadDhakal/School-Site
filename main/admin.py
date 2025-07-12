from django.contrib import admin
from .models import Teacher, Post, Comment, PhotoGallery, News

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title',)
    list_filter = ('date',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'date')
    search_fields = ('name', 'content')
    list_filter = ('date',)

@admin.register(PhotoGallery)
class PhotoGalleryAdmin(admin.ModelAdmin):
    list_display = ('caption', 'date')
    list_filter = ('date',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('headline', 'date', 'is_active')
    list_filter = ('is_active', 'date')
    search_fields = ('headline',)
