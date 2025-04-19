from django.db import models
from Authentication.models import User
from django.utils import timezone

# Create your models here.

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    image = models.URLField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_uploaded = models.DateTimeField(default=timezone.now)
    caption = models.CharField(max_length=100, blank=True)
    
    def owner_name(self):
        return self.owner.username
    
    def owner_pic(self):
        return self.owner.image

    def number_of_likes(self):
        return self.likes.count()  # Count the number of related like instances

    def __str__(self):
        return str(self.owner) + ", " + self.caption
    

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='likes',on_delete=models.CASCADE)
    date_liked = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('post', 'user')  # the combination is unique so each user can like a post atmost 
    
    def __str__(self):
        return f"{self.user} liked {self.post}"