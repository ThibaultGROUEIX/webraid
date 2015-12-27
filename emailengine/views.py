from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required()
def account_creation(request):
    data = {
        'username': request.user.username
    }
    return render(request, 'account_creation.html', data)
