from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Image, Profile, WelcomeEmailRecipients, Comment
from django.contrib.auth.decorators import login_required
from .email import send_welcome_email
from . forms import WelcomeEmailForm, SignUpForm, PostImageForm, CommentForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.contrib.auth.models import User
# Create your views here.


@login_required(login_url='/accounts/login/')
def home(request):
    images = Image.objects.all()
    print(images)
    profiles = Profile.objects.all()
    current_user = request.user
    specific_profile = Profile.objects.get(user=current_user)
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
    context = {"images": images, "current_user": current_user, "form": form,
               "profiles": profiles, "specific_profile": specific_profile}
    return render(request, 'index.html', context)


@login_required(login_url='/accounts/login/')
def profile(request, profile_id):
    current_profile = Profile.objects.get(id=profile_id)
    images = Image.objects.filter(profile=current_profile)

    follows = Profile.objects.get(id=request.user.id)
    is_follow = False
    if follows.following.filter(id=profile_id).exists():
        is_follow = True
    following = follows.following.all()
    followers = follows.user.followed_by.all()
    return render(request, 'profiles/profile.html', {"current_profile": current_profile, "images": images, "follows": follow, "is_follow": is_follow, "following": following, "followers": followers})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
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


@login_required(login_url='/accounts/login')
def new_post(request):
    profiles = Profile.get_all_profiles()
    profile1 = Profile.objects.get(id=request.user.id)
    # for profile in profiles:
    form = PostImageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            image = form.save(commit=False)
            image.profile = profile1
            image.save()
            return redirect(home)
    else:
        form = PostImageForm()
    return render(request, 'new_post.html', {"form": form})


def search_profiles(request):
    search_term = request.GET.get("profile")
    found_profiles = Profile.get_searched_profile(search_term)
    return render(request, 'search.html', {"found_profiles": found_profiles})


def comment(request, image_id):
    current_user = request.user
    current_image = Image.objects.get(id=image_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment_form = form.save(commit=False)
            comment_form.user = current_user
            comment_form.image = current_image
            comment_form.save()

    else:
        form = CommentForm()
    return render(request, 'comment.html', {"form": form, "current_image": current_image})


def detail(request, image_id):
    current_image = Image.objects.get(id=image_id)
    comment_details = Comment.objects.filter(image=current_image)
    is_liked = False
    if current_image.likes.filter(id=request.user.id).exists():
        is_liked = True

    try:
        image_details = Image.objects.get(id=image_id)
    except DoesNotExsist:
        raise Http404()

    return render(request, 'detail.html', {"image_details": image_details, "current_image": current_image, "comment_details": comment_details})


def like_post(request, image_id):
    post = Image.objects.get(id=image_id)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return redirect(detail, post.id)


def follow(request, user_id):
    follows = Profile.objects.get(id=request.user.id)
    user1 = User.objects.get(id=user_id)
    # user=Profile.objects.get(id=user_id)
    is_follow = False
    if follows.following.filter(id=user_id).exists():
        follows.following.remove(user1)
        is_follow = False
    else:
        follows.following.add(user1)
        is_follow = True
    return redirect(profile, user1.id)
