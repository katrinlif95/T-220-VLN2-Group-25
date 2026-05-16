from django.db import models

from django.contrib.auth.models import User


class Seller(models.Model):
    # Define allowed seller types (prevents typos and enforces valid values)
    SELLER_TYPE_CHOICES = [
        ("artist", "Artist"),
        ("gallery", "Gallery"),
    ]

    # Link each Seller to exactly one Django User
    # OneToOne means: one user can have at most one seller profile
    # If the user is deleted, the seller profile will also be deleted
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="seller_profile"
    )

    # Type of seller (Artist or Gallery)
    # Uses choices to restrict valid input values
    seller_type = models.CharField(
        max_length=20,
        choices=SELLER_TYPE_CHOICES
    )

    # Public name shown on the platform (can differ from username)
    display_name = models.CharField(max_length=255)

    # Required biography/description of the seller
    bio = models.TextField()

    # Short description shown on artwork cards/detail pages
    # Separate from the longer seller biography
    short_description = models.CharField(
        max_length=255,
        blank=True
    )

    # Public contact email shown on the platform
    # Separate from the Django User account email
    email = models.EmailField(blank=True)

    # Opening hours for galleries
    # Optional because artist profiles may not need this
    opening_hours = models.CharField(
        max_length=255,
        blank=True
    )

    # Required URLs for branding (logo and cover image)
    logo_url = models.URLField()
    cover_image_url = models.URLField()

    # Address fields:
    # According to requirements, these should ONLY be shown for galleries
    # Therefore they are optional in the database (blank=True)
    # but should be validated in forms if seller_type == "gallery"
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        # Human-readable name shown in admin and debug output
        return self.display_name
