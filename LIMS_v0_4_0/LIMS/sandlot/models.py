from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)

class Thread(models.Model):
    title = models.CharField(max_length=255)

class Post(models.Model):
    content = models.TextField()
    thread = models.ForeignKey('Thread', on_delete=models.PROTECT)

