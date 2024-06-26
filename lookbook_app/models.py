# lookbook_app/models.py
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Lookbook(models.Model):
    """
    Model representing a lookbook created by a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    overlay_image = CloudinaryField('overlay_images')
    orientation = models.CharField(max_length=10, choices=[('portrait', 'Portrait'), ('landscape', 'Landscape'), ('square', 'Square')], default='square')
    border_width = models.CharField(max_length=10, default='0px')
    border_color = models.CharField(max_length=10, default='black')

    def __str__(self):
        return self.title

class Profile(models.Model):
    """
    Model representing a user's profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = CloudinaryField('profile_pictures')
    profile_url = models.URLField(blank=True, null=True, default='https://res.cloudinary.com/yelenik/image/upload/avatar')
    bio = models.TextField(blank=True)
    my_lookbooks = models.ManyToManyField(Lookbook, blank=True)

    def __str__(self):
        return self.user.username


class LookbookImage(models.Model):
    """
    Model representing an image associated with a lookbook.
    """
    lookbook = models.ForeignKey(Lookbook, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('images')
    transformed_image = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Image for {self.lookbook.title}"
