from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.


class Image(models.Model):
    '''
    creating a class for the image model
    '''
    image_name = models.CharField(max_length=60)
    image_caption = HTMLField()
    comments = models.CharField(max_length=50)
    likes = models.PositiveIntegerField(default=0)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    post_image = models.ImageField(upload_to='posts/', null=True)

    def __str__(self):
        return self.image_name

    @classmethod
    def get_images(cls, image_id):
        images = cls.objects.all()
        return images


class Profile(models.Model):
    '''
    creating a profile model for each user
    '''
    avatar = models.ImageField(upload_to='avatar/', blank=True)
    bio = HTMLField()
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name
