from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Image
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    avatar = forms.ImageField()
    bio = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', 'avatar', 'bio')


class WelcomeEmailForm(forms.Form):
    your_name = forms.CharField(label='First Name', max_length=30)
    email = forms.EmailField(label='Email')


class PostImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image_name', 'image_caption', 'post_image']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        exclude = ['user']
