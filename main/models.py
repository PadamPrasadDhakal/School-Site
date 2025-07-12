from django.db import models

# Create your models here.

class Teacher(models.Model):
    LEVEL_CHOICES = [
        ('pre_primary', 'Pre Primary'),
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('higher_secondary', 'Higher Secondary'),
    ]
    name = models.CharField(max_length=100)
    pronouns = models.CharField(max_length=30, blank=True, help_text='e.g. she/her, he/him, they/them')
    subject = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='teachers/')
    bio = models.TextField(blank=True)
    about = models.TextField(blank=True, help_text='Short about me section')
    experience = models.TextField(blank=True, help_text='Experience details')
    education = models.TextField(blank=True, help_text='Education details')
    instagram = models.URLField(blank=True, default='https://www.instagram.com/')
    facebook = models.URLField(blank=True, default='https://www.facebook.com/')
    email = models.EmailField(blank=True, default='example@example.com')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='primary')

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', args=[str(self.pk)])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"

class PhotoAlbum(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='gallery/covers/')

    def __str__(self):
        return self.title

class PhotoGallery(models.Model):
    album = models.ForeignKey(PhotoAlbum, on_delete=models.CASCADE, related_name='photos', null=True, blank=True)
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption or f"Photo {self.id}"

class News(models.Model):
    headline = models.CharField(max_length=200)
    details = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.headline

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('news_detail', args=[str(self.pk)])
