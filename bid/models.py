from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from artwork.models import Artwork


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
        if self.amount <= 0:
            raise ValidationError(
                "Bid amount must be greater than zero."
            )

        # Prevent bids below starting price
        if (
            self.artwork
            and self.amount < self.artwork.starting_price
        ):
            raise ValidationError(
                "Bid amount cannot be lower than starting price."
            )

        # Prevent seller from bidding on own artwork
        if (
            self.artwork
            and self.artwork.seller.user == self.user
        ):
            raise ValidationError(
                "Seller cannot bid on their own artwork."
            )

        if self.artwork:
            # Find the highest other bid for the same artwork.
            # Compare the new bid amount only against other bids,
            # not against the previous version of this same bid.
            highest_other_bid = Bid.objects.filter(
                artwork=self.artwork
            ).exclude(
                pk=self.pk
            ).order_by(
                "-amount"
            ).first()

            # New amount must be higher than the highest other bid.
            if highest_other_bid and self.amount <= highest_other_bid.amount:
                raise ValidationError(
                    "Bid must be higher than current highest bid."
                )

    # String representation in admin and shell
    def __str__(self):
        return (
            f"{self.user.username} bid "
            f"{self.amount} on "
            f"{self.artwork.title}"
        )