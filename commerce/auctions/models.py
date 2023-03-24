from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class User(AbstractUser):
    pass


class Bid(models.Model):
    bidder = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, default=None)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    n = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.item} | Bids: {self.n}"


class Listing(models.Model):
    active = models.BooleanField(default=True)
    bids = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="item", null=True, default=None)
    datetime = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=2000)
    image_URL = models.URLField(blank=True)
    lister = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, default=None)
    title = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.lister} {self.title}"


class Comments():
    pass