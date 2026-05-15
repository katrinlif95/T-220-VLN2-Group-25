from bid.services import mark_bid_as_expired

def artwork_is_sold(artwork):
    """
    Return True if the artwork has an accepted
    or contingent bid.

    Accepted and contingent bids mean the artwork
    is no longer available for new bids.
    """

    return artwork.bids.filter(
        status__in=[
            "accepted",
            "contingent",
        ]
    ).exists()

def sync_artwork_status_from_bids(artwork):
    """
    Keep the saved artwork status in sync
    with accepted or contingent bids.
    """

    from artwork.models import Artwork

    if artwork_is_sold(artwork):
        artwork.status = Artwork.STATUS_SOLD
    else:
        artwork.status = Artwork.STATUS_AVAILABLE

    artwork.save(
        update_fields=["status"]
    )


def get_highest_bid(artwork):
    """
    Return the highest active bid placed
    on the artwork.

    Rejected, cancelled and expired bids
    are excluded.

    Returns:
        Bid object if active bids exist
        None if no active bids exist
    """

    # Only pending bids can expire
    pending_bids = artwork.bids.filter(
        status="pending"
    )

    # Update pending bids to expired
    # if expiration date has passed
    for bid in pending_bids:
        mark_bid_as_expired(bid)

    # Return highest active bid
    return artwork.bids.filter(
        status__in=[
            "pending",
            "accepted",
            "contingent",
        ]
    ).order_by(
        "-amount"
    ).first()


def get_current_highest_bid_amount(artwork):
    """
    Return the current highest bid amount.

    Returns:
        highest bid amount if bids exist
        None if no bids exist yet
    """

    highest_bid = get_highest_bid(artwork)

    if highest_bid:
        return highest_bid.amount

    return None


def add_artwork_display_status(artworks):
    """
    Add computed sold/available status
    to artwork objects for templates.

    This does not save anything to the database.
    """

    for artwork in artworks:
        artwork.is_sold = artwork_is_sold(
            artwork
        )

    return artworks