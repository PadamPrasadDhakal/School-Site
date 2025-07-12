from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('teachers/', views.teachers, name='teachers'),
    path('gallery/', views.gallery, name='gallery'),
    path('news/', views.news_list, name='news_list'),
    path('posts/', views.posts, name='posts'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
] 