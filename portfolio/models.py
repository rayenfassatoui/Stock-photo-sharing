from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Gallery(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='galleries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    is_public = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Galleries'
        ordering = ['-created_at']

class Photo(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    description = models.TextField(blank=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='photos')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=500, blank=True)
    allow_comments = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-uploaded_at']

class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.photo.title}'

    class Meta:
        ordering = ['-created_at']

class SharedAlbum(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='shared_with')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_galleries')
    can_comment = models.BooleanField(default=False)
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['gallery', 'shared_with']

    def __str__(self):
        return f'{self.gallery.name} shared with {self.shared_with.username}'
