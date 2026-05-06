from django.db import models

# Create your models here.
from django.contrib.auth.models import User


# Stores additional information for a user (separate from Django's built-in User)
class UserProfile(models.Model):

    # Defines allowed roles for the user
    ROLE_CHOICES = [
        ("buyer", "Buyer"),
        ("admin", "Admin"),
    ]

    # One-to-one link to Django User (each user has one profile)
    # If the user is deleted, the profile is also deleted
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    # Role of the user (restricted to predefined choices)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="buyer"
    )

    # Optional profile image URL
    profile_image_url = models.URLField(blank=True)

    # String representation shown in admin and debugging
    def __str__(self):
        return f"{self.user.username} profile"


# Stores contact and address information for a user
class ContactInfo(models.Model):

    # One-to-one link to Django User (each user has one contact info record)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="contact_info"
    )

    # Address and identification fields
    street_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20)

    # String representation shown in admin and debugging
    def __str__(self):
        return f"{self.user.username} contact info"
