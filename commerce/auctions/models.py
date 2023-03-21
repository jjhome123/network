from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=2000)
    price = models.IntegerField()
    image_URL = models.URLField(blank=True)

    def __str__(self):
        return f"{self.pk} {self.title}: ${self.price}"

class Bids():
    pass

class Comments():
    pass