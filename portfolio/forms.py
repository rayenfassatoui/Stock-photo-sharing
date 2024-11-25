from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Gallery, Photo, Comment

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['name', 'description', 'is_public']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'image', 'description', 'tags', 'allow_comments']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }

class ShareGalleryForm(forms.Form):
    email = forms.EmailField(label='Share with (email)')
    can_comment = forms.BooleanField(required=False, initial=True,
                                   label='Allow comments')
