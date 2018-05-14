import datetime as dt
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Image, Profile
from django.contrib.auth.decorators import login_required
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    images = Image.objects.all()
    profiles = Profile.objects.all()
    current_user = request.user
    if request.method == 'POST':
        form = WelcomeEmailForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = WelcomeEmailRecipients(name=name, email=email)
            recipient.save()
            send_welcome_email(name, email)

            HttpResponseRedirect('/accounts/login/')
    else:
        form = WelcomeEmailForm()
    context = {"images": images, "current_user": current_user, "form": form, "profiles": profiles}
    return render(request, 'index.html', context)


def explore(request):
    images = Image.get_images()

    return render(request, 'base.html', {"images": images})


@login_required(login_url='/accounts/login/')
def profile(request):
    test = 'Profile route Working'
    current_user = request.user
    images = Image.objects.filter(poster=request.user)
    profiles = Profile.objects.filter(user=request.user)
    content = {
        "test": test,
        "current_user": current_user,
        "images": images,
        "profiles": profiles
    }
    return render(request, 'profiles/profile.html', content)
