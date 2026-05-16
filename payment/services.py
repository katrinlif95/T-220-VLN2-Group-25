from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from artwork.models import ArtworkImage
from bid.models import Bid

from .models import Payment

def get_finalize_bid_or_404(bid_id):
    """
    Get bid used in the finalize checkout flow.

    Also prefetch artwork images in display order
    so templates can show the correct first image.
    """

    return get_object_or_404(
        Bid.objects.select_related(
            "artwork",
            "artwork__seller",
        ).prefetch_related(
            Prefetch(
                "artwork__images",
                queryset=ArtworkImage.objects.order_by("order"),
                to_attr="ordered_images",
            )
        ),
        id=bid_id,
    )

def can_finalize_bid(bid):
    """
    Return True if a bid is allowed to continue
    through the payment/finalization flow.
    """

    return bid.status in ["accepted", "contingent"]

def bid_has_completed_payment(bid):

    # Check if bid already has a completed payment
    return Payment.objects.filter(
        bid=bid,
        status=Payment.STATUS_COMPLETED
    ).exists()

def validate_finalize_flow_access(bid, user):
    if bid.user != user:
        return {
            "is_valid": False,
            "error": "You are not allowed to finalize this bid."
        }

    if bid_has_completed_payment(bid):
        return {
            "is_valid": False,
            "error": "This bid has already been finalized."
        }


    if bid.status not in ["accepted", "contingent"]:
        return {
            "is_valid": False,
            "error": "Only accepted or contingent bids can be finalized."
        }

    return {
        "is_valid": True,
        "error": ""
    }

def reject_other_pending_bids(bid):
    """
    Reject all other pending bids on the same artwork
    after successful payment completion.
    """

    Bid.objects.filter(
        artwork=bid.artwork,
        status=Bid.STATUS_PENDING
    ).exclude(
        id=bid.id
    ).update(
        status=Bid.STATUS_REJECTED
    )