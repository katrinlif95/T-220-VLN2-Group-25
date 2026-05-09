# Business logic for payment/finalization flow

from .models import Payment


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


def validate_finalize_flow_access(bid):

    # Bid must be accepted or contingent
    if not can_finalize_bid(bid):

        return {
            "is_valid": False,
            "error": "This bid cannot be finalized."
        }

    # Bid must not already have a completed payment
    if bid_has_completed_payment(bid):

        return {
            "is_valid": False,
            "error": "This bid has already been paid."
        }

    return {
        "is_valid": True,
        "error": None
    }