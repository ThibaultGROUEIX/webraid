from django.views.generic import ListView, FormView
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render

def test(request):
    return HttpResponse("<p>Test Reussi</p>")

