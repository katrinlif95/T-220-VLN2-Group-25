from django.utils import timezone
from .models import Bid
from payment.models import Payment
from django.db.models import Exists, OuterRef, Subquery

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

def get_bid_alert_counts(user):
    """
    Return bid counts shown on user profile/account pages.

    Counts:
    - unfinalized: accepted/contingent bids without completed payment
    - outbid: pending bids where another bid is currently higher
    """

    completed_payment_exists = Payment.objects.filter(
        bid=OuterRef("pk"),
        status="completed",
    )

    highest_bid_amount = Bid.objects.filter(
        artwork=OuterRef("artwork_id"),
        status__in=[
            "pending",
            "accepted",
            "contingent",
        ],
    ).order_by(
        "-amount"
    ).values(
        "amount"
    )[:1]

    user_bids = Bid.objects.filter(
        user=user,
    ).annotate(
        is_finalized=Exists(completed_payment_exists),
        artwork_annotated_highest_bid_amount=Subquery(
            highest_bid_amount
        ),
    )

    unfinalized_count = user_bids.filter(
        status__in=[
            "accepted",
            "contingent",
        ],
        is_finalized=False,
    ).count()

    outbid_count = user_bids.filter(
        status="pending",
        amount__lt=Subquery(highest_bid_amount),
    ).count()

    pending_count = Bid.objects.filter(
        user=user,
        status="pending",
    ).count()

    return {
        "unfinalized_count": unfinalized_count,
        "outbid_count": outbid_count,
        "pending_count": pending_count,
    }
