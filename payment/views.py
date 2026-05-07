from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

# Import Bid model
from bid.models import Bid


def contact_information(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Only accepted or contingent bids
    # can be finalized
    if bid.status not in ["accepted", "contingent"]:

        # Show error message
        messages.error(
            request,
            "Only accepted bids can be finalized."
        )

        # Redirect user back to my bids page
        return redirect("account-bids")

    # If contact information form is submitted
    if request.method == "POST":

        # Later:
        # Save contact information here

        # Redirect user to payment details step
        return redirect(
            "finalize-payment",
            bid_id=bid.id
        )

    # Render contact information page
    return render(request, "payment/contact_information.html", {

        # Send bid to template
        "bid": bid,

        # Send related artwork to template
        "artwork": bid.artwork
    })

def payment_details(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Only accepted or contingent bids
    # can continue to payment details
    if bid.status not in ["accepted", "contingent"]:
        messages.error(
            request,
            "Only accepted bids can be finalized."
        )
        return redirect("account-bids")

    # If payment details form is submitted
    if request.method == "POST":

        # Later:
        # Save selected payment method/details here

        # Redirect user to review step
        return redirect(
            "finalize-review",
            bid_id=bid.id
        )

    # Render payment details page
    return render(request, "payment/payment_details.html", {

        # Send bid to template
        "bid": bid,

        # Send related artwork to template
        "artwork": bid.artwork
    })

def review_payment(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Only accepted or contingent bids
    # can continue to review
    if bid.status not in ["accepted", "contingent"]:
        messages.error(
            request,
            "Only accepted bids can be finalized."
        )
        return redirect("account-bids")

    # Render review page before final confirmation
    return render(request, "payment/finalize_review.html", {
        "bid": bid,
        "artwork": bid.artwork,
        "show_success_modal": False
    })


def confirm_payment(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Confirm should only happen through POST
    if request.method != "POST":
        return redirect("finalize-review", bid_id=bid.id)

    # Only accepted or contingent bids
    # can be confirmed
    if bid.status not in ["accepted", "contingent"]:
        messages.error(
            request,
            "Only accepted bids can be finalized."
        )
        return redirect("account-bids")

    # Later:
    # Mark bid as paid/finalized

    # Render review page again with success modal open
    return render(request, "payment/finalize_review.html", {
        "bid": bid,
        "artwork": bid.artwork,
        "show_success_modal": True
    })
