from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from models import *

def index(request):

    return render(request, 'lrapp/lrIndex.html')

def create(request):
    result = User.objects.validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)

        return redirect(reverse('lr_index'))

    request.session["name"] = result.first_name

    return redirect(reverse('lr_success'))

def success(request):
    if not "name" in request.session:
        messages.error(request, "You must log in or register!")
        return redirect(reverse('lr_index'))

    return render(request, 'lrapp/lrSuccess.html')

def login(request):
    result = User.objects.login(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect(reverse('lr_index'))

    request.session["name"] = result.first_name

    return redirect(reverse('lr_success'))

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')
