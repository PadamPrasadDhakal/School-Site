from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher, Post, Comment, PhotoGallery, News
from django.utils import timezone

# Home page: school info, news bar, latest posts

def home(request):
    school_info = {
        'name': 'Balabhadra Janat Higher Secondary School',
        'address': 'Mechinagar-11, Dhaijan, Jhapa',
        'phone': '023460046',
    }
    news = News.objects.filter(is_active=True).order_by('-date')[:5]
    latest_posts = Post.objects.order_by('-date')[:3]
    return render(request, 'main/home.html', {
        'school_info': school_info,
        'news': news,
        'latest_posts': latest_posts,
    })

# Teachers page

def teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'main/teachers.html', {'teachers': teachers})

# Gallery page

def gallery(request):
    photos = PhotoGallery.objects.order_by('-date')
    return render(request, 'main/gallery.html', {'photos': photos})

# News page

def news_list(request):
    news = News.objects.filter(is_active=True).order_by('-date')
    return render(request, 'main/news_list.html', {'news': news})

# Posts page

def posts(request):
    posts = Post.objects.order_by('-date')
    return render(request, 'main/posts.html', {'posts': posts})

# Post detail with comments

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.order_by('-date')
    if request.method == 'POST':
        name = request.POST.get('name')
        content = request.POST.get('content')
        if name and content:
            Comment.objects.create(post=post, name=name, content=content, date=timezone.now())
            return redirect('post_detail', pk=post.pk)
    return render(request, 'main/post_detail.html', {'post': post, 'comments': comments})
