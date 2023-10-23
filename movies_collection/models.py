from django.db import models
import uuid
from account.models import User
# Create your models here.


class MovieCollection(models.Model):
    collection_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250)
    description = models.TextField()
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Movie(models.Model):
    uuid = models.UUIDField()
    title = models.CharField(max_length=250)
    description = models.TextField()
    genres= models.CharField(max_length=250)
    collection = models.ForeignKey(MovieCollection, on_delete=models.CASCADE, related_name='movies')
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_movies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


