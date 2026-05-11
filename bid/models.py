from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from artwork.models import Artwork
from django.utils import timezone


class Bid(models.Model):

    # Bid status constants
    STATUS_PENDING = "pending"
    STATUS_ACCEPTED = "accepted"
    STATUS_REJECTED = "rejected"
    STATUS_CONTINGENT = "contingent"
    STATUS_CANCELLED = "cancelled"

    # Available status choices
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_CONTINGENT, "Contingent"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    # User who placed the bid
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bids"
    )

    # Artwork being bid on
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name="bids"
    )

    # Bid amount
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Current bid status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    # Bid expiration date
    expires_at = models.DateTimeField()

    # Set when bid is cancelled
    cancelled_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # Automatically set on creation
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # Automatically updated on save
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def clean(self):

        # Prevent zero or negative bids
        if self.amount is not None and self.amount <= 0:
            raise ValidationError(
                "Bid amount must be greater than zero."
            )

        # Prevent seller from bidding on own artwork
        if (
            self.artwork_id
            and self.user_id
            and self.artwork.seller.user_id == self.user_id
        ):
            raise ValidationError(
                "Seller cannot bid on their own artwork."
            )


    # String representation in admin and shell
    def __str__(self):
        return (
            f"{self.user.username} bid "
            f"{self.amount} on "
            f"{self.artwork.title}"
        )