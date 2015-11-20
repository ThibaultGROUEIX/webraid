
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from forms import CategoryForm, AlbumForm, PictureForm
from models import Category, Album, Picture

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





# Create your views here.
