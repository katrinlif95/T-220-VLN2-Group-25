from django import forms
from django.utils import timezone
from .models import Bid


class BidForm(forms.ModelForm):
    """
    Form used for submitting artwork bids.
    """

    class Meta:
        model = Bid

        fields = [
            "amount",
            "expires_at",
        ]

        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "placeholder": "Enter higher than current bid",
                    "step": "0.01",
                    "min": "1",
                }
            ),
            "expires_at": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

        labels = {
            "amount": "Amount",
            "expires_at": "Expiration date",
        }

    def __init__(self, *args, artwork=None, existing_bid=None, **kwargs):
        """
        Store artwork and existing bid for validation.
        """

        super().__init__(*args, **kwargs)

        self.artwork = artwork
        self.existing_bid = existing_bid

    def clean_amount(self):
        """
        Validate bid amount against starting price
        and current highest bid.
        """

        amount = self.cleaned_data.get("amount")

        if amount is None:
            return amount

        if self.artwork and amount < self.artwork.starting_price:
            raise forms.ValidationError(
                "Bid amount cannot be lower than starting price."
            )

        if self.artwork:

            highest_bid = Bid.objects.filter(
                artwork=self.artwork,
                status=Bid.STATUS_PENDING
            )

            # If user is resubmitting an existing bid,
            # do not compare the amount against itself
            if self.existing_bid:
                highest_bid = highest_bid.exclude(
                    pk=self.existing_bid.pk
                )

            highest_bid = highest_bid.order_by(
                "-amount"
            ).first()

            if highest_bid and amount <= highest_bid.amount:
                raise forms.ValidationError(
                    "Bid must be higher than current highest bid."
                )

        return amount

    def clean_expires_at(self):
        """
        Validate that expiration date is in the future.
        """

        expires_at = self.cleaned_data.get("expires_at")

        if expires_at is None:
            return expires_at

        if expires_at <= timezone.now():
            raise forms.ValidationError(
                "Expiration date must be in the future."
            )

        return expires_at

    def clean(self):
        """
        Validate that pending resubmitted bids contain
        at least one actual change.

        Rejected bids may be resubmitted unchanged.
        """

        cleaned_data = super().clean()

        amount = cleaned_data.get("amount")
        expires_at = cleaned_data.get("expires_at")

        # Prevent resubmitting identical data
        # only when the existing bid is still pending
        if (
                self.existing_bid
                and self.existing_bid.status == Bid.STATUS_PENDING
                and amount == self.existing_bid.amount
                and expires_at == self.existing_bid.expires_at
        ):
            raise forms.ValidationError(
                "Please update your bid before resubmitting."
            )

        return cleaned_data

