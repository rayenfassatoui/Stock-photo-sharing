from django.contrib import admin
from .models import Gallery, Photo, Comment, SharedAlbum

# Register your models here.

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'is_public')
    list_filter = ('is_public', 'created_at')
    search_fields = ('name', 'description', 'user__username')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'gallery', 'uploaded_at', 'allow_comments')
    list_filter = ('allow_comments', 'uploaded_at', 'gallery')
    search_fields = ('title', 'description', 'tags')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username')

@admin.register(SharedAlbum)
class SharedAlbumAdmin(admin.ModelAdmin):
    list_display = ('gallery', 'shared_with', 'can_comment', 'shared_at')
    list_filter = ('can_comment', 'shared_at')
    search_fields = ('gallery__name', 'shared_with__username')
