from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Image, Profile, WelcomeEmailRecipients
from django.contrib.auth.decorators import login_required
from .email import send_welcome_email
from . forms import WelcomeEmailForm, SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

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


@login_required(login_url='/accounts/login/')
def profile(request, profile_id):
    current_profile = Profile.objects.get(id=profile_id)
    images = Image.objects.filter(profile=current_profile)

    return render(request, 'profiles/profile.html', {"current_profile": current_profile, "images": images})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance
            user.profile.avatar = form.cleaned_data.get('avatar')
            user.profile.bio = form.cleaned_data.get('bio')
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
