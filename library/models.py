from django.db import models
"""
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
"""

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    bio = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    
    
    def __str__(self):
            return self.title
