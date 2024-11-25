from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Gallery URLs
    path('gallery/create/', views.gallery_create, name='gallery_create'),
    path('gallery/<slug:slug>/', views.gallery_detail, name='gallery_detail'),
    path('gallery/<slug:slug>/edit/', views.gallery_edit, name='gallery_edit'),
    path('gallery/<slug:slug>/share/', views.share_gallery, name='share_gallery'),
    
    # Photo URLs
    path('gallery/<int:gallery_id>/upload/', views.photo_upload, name='photo_upload'),
    path('photo/<int:pk>/', views.photo_detail, name='photo_detail'),
    path('photo/<int:pk>/delete/', views.photo_delete, name='photo_delete'),
    
    # Search
    path('search/', views.search_photos, name='search_photos'),
]
