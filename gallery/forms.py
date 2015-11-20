from django import forms

from models import Category, Album, Picture


# Default base forms
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['titre',  'caption']


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['titre',  'caption', 'category']




class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['titre',  'caption', 'album', 'image' ]
