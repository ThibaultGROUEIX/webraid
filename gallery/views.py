
from django.shortcuts import redirect
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from forms import CategoryForm, AlbumForm, PictureForm
from models import Category, Album, Picture
from webraid.settings  import MEDIA_ROOT


from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response

from forms import UploadFileForm
from models import UploadFile


def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadFile(file = request.FILES['file'])
            new_file.save()

            return HttpResponseRedirect(reverse('gallery:home'))
    else:
        form = UploadFileForm()

    data = {'form': form}
    return render_to_response('gallery/index.html', data, context_instance=RequestContext(request))


def test(request):

    return HttpResponse("<p> Test </p>")

def new_category(request):
    sauvegarde = False

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = Category()
            category.titre = form.cleaned_data["titre"]
            category.caption = form.cleaned_data["caption"]
            category.coverImage = form.cleaned_data["coverImage"]
            #note: you have to fill the foreign key before saving
            category.createur = request.user
            #note : you have to save the instance in the database before adding a maytomanyfiel
            category.save()
            category.contributeurs.add(request.user)
            category.save()
            sauvegarde = True
    else:
        form = CategoryForm()

    return render(request, 'gallery/new_category.html', locals())

def new_album(request):
    sauvegarde = False

    if request.method == "POST":
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = Album()
            album.coverImage = form.cleaned_data["coverImage"]
            album.titre = form.cleaned_data["titre"]
            album.caption = form.cleaned_data["caption"]
            album.category = form.cleaned_data["category"]
            #note: you have to fill the foreign key before saving
            album.createur = request.user
            #note : you have to save the instance in the database before adding a maytomanyfiel
            album.save()
            album.contributeurs.add(request.user)
            album.save()
            sauvegarde = True
    else:
        form = AlbumForm()

    return render(request, 'gallery/new_album.html', locals())




def view_photo(request, id_category, id_album, id_photo):
    photo = Picture.objects.get(id = id_photo)
    return render(request, 'gallery/view_photo.html', locals())


def new_photo(request):
    sauvegarde = False

    if request.method == "POST":
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            photo = Picture()
            photo.titre = form.cleaned_data["titre"]
            photo.caption = form.cleaned_data["caption"]
            photo.album = form.cleaned_data["album"]
            photo.image = form.cleaned_data["image"]
            #note: you have to fill the foreign key before saving
            photo.createur = request.user
            #note : you have to save the instance in the database before adding a maytomanyfiel
            photo.save()
            sauvegarde = True
    else:
        form = PictureForm()

    return render(request, 'gallery/new_picture.html', locals())



# Create your views here.
