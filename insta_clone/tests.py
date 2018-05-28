from django.test import TestCase
from django.contrib.auth.models import User
from .models import Image, Profile, Comment


class TestImageClass(TestCase):
    """test class for Image model"""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "secret")
        self.new_profile = Profile(avatar='profiles/profile.jpg',
                                   bio="this is a test bio", user=self.user
                                   )
        self.new_profile.save()

        self.new_image = Image(post_image='photos/test.jpg', image_name='testImage',
                               image_caption="this is a test image", profile=self.new_profile)

    def test_instance_true(self):
        self.new_image.save()
        self.assertTrue(isinstance(self.new_image, Image))

    def tearDown(self):
        Image.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
