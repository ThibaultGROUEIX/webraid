
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse




def test(request):
    return H(revterse('profiles-list'))


def view_logged_out(request):
    return render(request, 'registration/logout.html')




# Create your views here.
