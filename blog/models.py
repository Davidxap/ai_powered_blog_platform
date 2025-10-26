from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, blank=False)


    def __str__(self):
        return self.title
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.username} on '{self.post.title}'"

