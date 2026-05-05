from django.db import models

# Create your models here.
from seller.models import Seller


class Artwork(models.Model):

    # Artwork status choices
    STATUS_CHOICES = [
        ("available", "Available"),
        ("sold", "Sold"),
    ]


    # Each artwork belongs to one seller
    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name="artworks"
    )

    # Basic artwork info
    title = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)

    medium = models.CharField(max_length=100)
    style = models.CharField(max_length=100)

    dimensions = models.CharField(max_length=100)
    year = models.IntegerField()

    edition = models.CharField(max_length=100)
    provenance = models.TextField()

    # Pricing
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Status (e.g. available / sold)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available"
    )

    # When listed
    listed_at = models.DateTimeField(auto_now_add=True)
            # auto_now_add=True sets the timestamp when the object is created

    def __str__(self):
        return self.title