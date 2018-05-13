import datetime as dt
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Image, Profile

#from .email import send_welcome_email
from django.contrib.auth.decorators import login_required

# Create your views here.


def explore(request):
    images = Image.get_images()

    return render(request, 'base.html', {"images": images})
