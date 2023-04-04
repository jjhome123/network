from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    post = models.CharField(max_length=2000)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"({self.pk}){self.poster}:{self.datetime}"

class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, related_name="liked_posts")
    status = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, default=None, related_name="liked_by")

    def __str__(self):
        return f"{self.liker} likes {self.post}: {self.status}"

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, related_name="follower")
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, related_name="being_followed")

    def __str__(self):
        return f"{self.user} follows {self.following_user}"