from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class WelcomeEmailRecipients(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()


class Profile(models.Model):
    '''
    creating a profile model for each user
    '''
    avatar = models.ImageField(upload_to='avatar/', blank=True)
    bio = HTMLField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    def __str__(self):
        return self.first_name


class Image(models.Model):
    '''
    creating a class for the image model
    '''
    image_name = models.CharField(max_length=60)
    image_caption = HTMLField()
    comments = models.CharField(max_length=50)
    likes = models.PositiveIntegerField(default=0)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to='posts/', null=True)
    poster = models.ForeignKey(User, default=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.image_name

    @classmethod
    def get_images(cls):
        images = cls.objects.all()
        return images
