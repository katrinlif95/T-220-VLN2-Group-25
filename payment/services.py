# Business logic for payment/finalization flow


def can_finalize_bid(bid):
    """
    Return True if a bid is allowed to continue
    through the payment/finalization flow.
    """
    return bid.status in ["accepted", "contingent"]