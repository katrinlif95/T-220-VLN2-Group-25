from django.db import models

# Create your models here.
from seller.models import Seller


class Artwork(models.Model):

    STATUS_AVAILABLE = "available"
    STATUS_SOLD = "sold"

    # Artwork status choices
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, "Available"),
        (STATUS_SOLD, "Sold"),
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

    # Controls artwork order on listing pages
    # Lower numbers appear first
    display_order = models.PositiveIntegerField(default=0)

    # Featured/highlighted artwork
    highlighted = models.BooleanField(default=False)

    # Status (e.g. available / sold)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_AVAILABLE
    )

    # When listed
    listed_at = models.DateTimeField()
            # auto_now_add=True sets the timestamp when the object is created

    def __str__(self):
        return self.title

class ArtworkImage(models.Model):
    # Each image belongs to one artwork
    # One artwork can have many images
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name="images"
    )

    # URL of this specific image
    image_url = models.URLField()

    # Required alt text for accessibility
    alt_text = models.CharField(max_length=255)

    # Controls the order of images in a gallery/carousel
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.artwork.title} image {self.order}"