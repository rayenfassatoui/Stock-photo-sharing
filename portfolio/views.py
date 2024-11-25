from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .forms import (UserRegistrationForm, GalleryForm, PhotoForm,
                   PhotoBulkUploadForm, CommentForm, ShareGalleryForm)
from .models import Gallery, Photo, Comment, SharedAlbum, User

def home(request):
    galleries = Gallery.objects.filter(is_public=True).order_by('-created_at')[:9]
    return render(request, 'portfolio/home.html', {'galleries': galleries})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    user_galleries = Gallery.objects.filter(user=request.user).order_by('-created_at')
    shared_galleries = Gallery.objects.filter(shared_with__shared_with=request.user)
    return render(request, 'portfolio/dashboard.html', {
        'user_galleries': user_galleries,
        'shared_galleries': shared_galleries
    })

@login_required
def gallery_create(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST)
        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.user = request.user
            gallery.save()
            messages.success(request, 'Gallery created successfully!')
            return redirect('gallery_detail', slug=gallery.slug)
    else:
        form = GalleryForm()
    return render(request, 'portfolio/gallery_form.html', {'form': form})

@login_required
def gallery_edit(request, slug):
    gallery = get_object_or_404(Gallery, slug=slug, user=request.user)
    if request.method == 'POST':
        form = GalleryForm(request.POST, instance=gallery)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery updated successfully!')
            return redirect('gallery_detail', slug=gallery.slug)
    else:
        form = GalleryForm(instance=gallery)
    return render(request, 'portfolio/gallery_form.html', {'form': form, 'gallery': gallery})

def gallery_detail(request, slug):
    gallery = get_object_or_404(Gallery, slug=slug)
    if not gallery.is_public and request.user != gallery.user:
        shared = SharedAlbum.objects.filter(gallery=gallery, shared_with=request.user).exists()
        if not shared:
            messages.error(request, 'You do not have permission to view this gallery.')
            return redirect('home')
    
    photos = gallery.photos.all().order_by('-uploaded_at')
    paginator = Paginator(photos, 12)
    page = request.GET.get('page')
    photos = paginator.get_page(page)
    
    return render(request, 'portfolio/gallery_detail.html', {
        'gallery': gallery,
        'photos': photos,
    })

@login_required
def photo_upload(request, gallery_slug):
    gallery = get_object_or_404(Gallery, slug=gallery_slug, user=request.user)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.gallery = gallery
            photo.save()
            messages.success(request, 'Photo uploaded successfully!')
            return redirect('gallery_detail', slug=gallery.slug)
    else:
        form = PhotoForm()
    return render(request, 'portfolio/photo_form.html', {'form': form, 'gallery': gallery})

@login_required
def photo_bulk_upload(request):
    if request.method == 'POST':
        form = PhotoBulkUploadForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            gallery = form.cleaned_data['gallery']
            files = request.FILES.getlist('images')
            for file in files:
                Photo.objects.create(
                    gallery=gallery,
                    image=file,
                    title=file.name
                )
            messages.success(request, f'{len(files)} photos uploaded successfully!')
            return redirect('gallery_detail', slug=gallery.slug)
    else:
        form = PhotoBulkUploadForm(request.user)
    return render(request, 'portfolio/photo_bulk_upload.html', {'form': form})

@login_required
def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if not photo.gallery.is_public and request.user != photo.gallery.user:
        shared = SharedAlbum.objects.filter(gallery=photo.gallery, shared_with=request.user).exists()
        if not shared:
            messages.error(request, 'You do not have permission to view this photo.')
            return redirect('home')
    
    if request.method == 'POST' and photo.allow_comments:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('photo_detail', pk=pk)
    else:
        form = CommentForm()
    
    comments = photo.comments.all().order_by('-created_at')
    return render(request, 'portfolio/photo_detail.html', {
        'photo': photo,
        'form': form,
        'comments': comments
    })

@login_required
def share_gallery(request, slug):
    gallery = get_object_or_404(Gallery, slug=slug, user=request.user)
    if request.method == 'POST':
        form = ShareGalleryForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            can_comment = form.cleaned_data['can_comment']
            try:
                user = User.objects.get(email=email)
                SharedAlbum.objects.create(
                    gallery=gallery,
                    shared_with=user,
                    can_comment=can_comment
                )
                messages.success(request, f'Gallery shared with {email}!')
            except User.DoesNotExist:
                messages.error(request, f'No user found with email {email}')
            return redirect('gallery_detail', slug=slug)
    else:
        form = ShareGalleryForm()
    return render(request, 'portfolio/share_gallery.html', {'form': form, 'gallery': gallery})

@login_required
def search_photos(request):
    query = request.GET.get('q', '')
    if query:
        photos = Photo.objects.filter(
            Q(gallery__user=request.user) |
            Q(gallery__shared_with__shared_with=request.user),
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        ).distinct()
    else:
        photos = Photo.objects.none()
    
    return render(request, 'portfolio/search_results.html', {
        'photos': photos,
        'query': query
    })
