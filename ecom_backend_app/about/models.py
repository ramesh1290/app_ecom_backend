from django.db import models
from cloudinary.models import CloudinaryField

class About(models.Model):
    title = models.CharField(max_length=200)
    description_1 = models.TextField()
    description_2 = models.TextField(blank=True, null=True)

    mission_title = models.CharField(max_length=100)
    mission_desc = models.TextField()

    vision_title = models.CharField(max_length=100)
    vision_desc = models.TextField()

    image = CloudinaryField('image', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title