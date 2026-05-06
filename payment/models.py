from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from bid.models import Bid

class Payment(models.Model):

    # Payment status constants
    STATUS_PENDING = "pending"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"

    # Available payment status choices
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED, "Failed"),
    ]

    # Payment method constants
    METHOD_CREDIT_CARD = "credit_card"
    METHOD_BANK_TRANSFER = "bank_transfer"
    METHOD_WIRE_TRANSFER = "wire_transfer"

    # Available payment method choices
    PAYMENT_METHOD_CHOICES = [
        (METHOD_CREDIT_CARD, "Credit card"),
        (METHOD_BANK_TRANSFER, "Bank transfer"),
        (METHOD_WIRE_TRANSFER, "Wire transfer"),
    ]

    # User making the payment
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    # Bid connected to the payment
    bid = models.ForeignKey(
        Bid,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    # Payment amount
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # Selected payment method
    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES
    )

    # Current payment status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    # Automatically set when payment is created
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):

        # Prevent zero or negative payments
        if self.amount <= 0:
            raise ValidationError(
                "Payment amount must be greater than zero."
            )

        # Payment amount must match the bid amount
        if self.bid and self.amount != self.bid.amount:
            raise ValidationError(
                "Payment amount must match bid amount."
            )

        # Only accepted or contingent bids can be paid
        if self.bid and self.bid.status not in [
            Bid.STATUS_ACCEPTED,
            Bid.STATUS_CONTINGENT,
        ]:
            raise ValidationError(
                "Only accepted or contingent bids can be paid."
            )

    # String representation in admin and shell
    def __str__(self):
        return (
            f"{self.user.username} paid "
            f"{self.amount} for "
            f"{self.bid.artwork.title}"
        )