from django.utils import timezone

from .models import Bid


# Check whether a bid has passed its expiration date
def is_bid_expired(bid):

    return bid.expires_at < timezone.now()


# Update bid status to expired
# if the expiration date has passed
def mark_bid_as_expired(bid):

    # Only pending bids can expire
    if (
        bid.status == Bid.STATUS_PENDING
        and is_bid_expired(bid)
    ):

        bid.status = Bid.STATUS_EXPIRED

        # Save only the updated status field
        bid.save(update_fields=["status"])

    return bid