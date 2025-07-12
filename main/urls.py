from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teachers/', views.teachers, name='teachers'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<int:pk>/', views.album_detail, name='album_detail'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('posts/', views.posts, name='posts'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('teachers/<int:pk>/', views.teacher_detail, name='teacher_detail'),
] 