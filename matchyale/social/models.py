from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='profile_pics')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self): # let the form deal with redirect
        return reverse("moment-detail", kwargs={"pk": self.pk})
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    def get_absolute_url(self): # let the form deal with redirect
        return reverse("moment-detail", kwargs={"pk": self.pk})
    def __str__(self):
        return '%s ' % (self.post.title)
    
    