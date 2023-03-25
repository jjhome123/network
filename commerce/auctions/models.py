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
    bids = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="item", blank=True, null=True, default=None)
    datetime = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=2000)
    image_URL = models.URLField(blank=True)
    lister = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, default=None)
    title = models.CharField(max_length=64)
    category = models.CharField(max_length=64, blank=True, null=True, default=None)

    def __str__(self):
        return f"{self.id} | {self.title}"


class Comment(models.Model):
    commenter = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, default=None)
    comment = models.CharField(max_length=2000)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, default=None)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.comment}"


class Watchlist(models.Model):
    watcher = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, default=None)
    is_watchlist = models.BooleanField(default=False)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"{self.item} is in {self.watcher}'s watchlist: {self.is_watchlist}"

