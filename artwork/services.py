

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


def get_highest_bid(artwork):
    """
    Return the highest bid placed on the artwork.

    Returns:
        Bid object if bids exist
        None if no bids exist
    """

    return artwork.bids.order_by(
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