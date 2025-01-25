from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
# Create your models here.
from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField()
    videoUrl = models.CharField(max_length=255)
    image = CloudinaryField('image')
    ingredients = models.JSONField()
    author = models.ForeignKey(User,models.CASCADE)

    def __str__(self):
        return self.name
    
class Like(models.Model) :
    recipe = models.ForeignKey(Recipe, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)

    class Meta:
        unique_together = ('recipe', 'user') 
