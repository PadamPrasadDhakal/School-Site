from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher, Post, Comment, PhotoGallery, News, PhotoAlbum
from django.utils import timezone

# Home page: school info, news bar, latest posts

def get_news():
    return News.objects.filter(is_active=True).order_by('-date')[:5]

def home(request):
    school_info = {
        'name': 'Balabhadra Janata Higher Secondary School',
        'address': 'Mechinagar-11, Dhaijan, Jhapa',
        'phone': '023460046',
    }
    news = get_news()
    latest_posts = Post.objects.order_by('-date')[:3]
    return render(request, 'main/home.html', {
        'school_info': school_info,
        'news': news,
        'latest_posts': latest_posts,
    })

# Teachers page

def teachers(request):
    level_order = ['higher_secondary','secondary', 'primary', 'pre_primary' ]
    teachers = list(Teacher.objects.all())
    teachers.sort(key=lambda t: (level_order.index(t.level) if t.level in level_order else 99, t.name))
    news = get_news()
    return render(request, 'main/teachers.html', {'teachers': teachers, 'news': news})

# Gallery page

def gallery(request):
    albums = PhotoAlbum.objects.all()
    news = get_news()
    return render(request, 'main/gallery.html', {'albums': albums, 'news': news})

def album_detail(request, pk):
    album = get_object_or_404(PhotoAlbum, pk=pk)
    photos = album.photos.order_by('-date')
    news = get_news()
    return render(request, 'main/album_detail.html', {'album': album, 'photos': photos, 'news': news})

# News page

def news_list(request):
    news = get_news()
    return render(request, 'main/news_list.html', {'news': news})

# Posts page

def posts(request):
    posts = Post.objects.order_by('-date')
    news = get_news()
    return render(request, 'main/posts.html', {'posts': posts, 'news': news})

# Post detail with comments

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.order_by('-date')
    news = get_news()
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')
        if name and content:
            Comment.objects.create(post=post, name=name, content=content, date=timezone.now())
            return redirect('post_detail', pk=post.pk)
    return render(request, 'main/post_detail.html', {'post': post, 'comments': comments, 'news': news})

def news_detail(request, pk):
    news_item = get_object_or_404(News, pk=pk)
    news = get_news()
    return render(request, 'main/news_detail.html', {'news_item': news_item, 'news': news})
