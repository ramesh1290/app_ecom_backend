from django.db import models

class WhyChooseUs(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100)  # store icon class name
    order = models.PositiveIntegerField(default=0)  
    def __str__(self):
        return self.title