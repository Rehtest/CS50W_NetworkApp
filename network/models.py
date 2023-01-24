from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="user_followers")

    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return User.objects.filter(followers=self).count()

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    post = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likers")
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}: {self.post} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']