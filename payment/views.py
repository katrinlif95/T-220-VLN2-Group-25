from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect

# Import Bid model
from bid.models import Bid

# Import payment business logic
from .services import can_finalize_bid


def contact_information(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Only accepted or contingent bids
    # can continue through finalize flow
    if not can_finalize_bid(bid):

        # Redirect user back to my bids page
        # Optional:
        # Add error message here later if needed
        return redirect("account-bids")

    # If contact information form is submitted
    if request.method == "POST":

        # Save contact information in session
        # so it persists when navigating between finalize steps
        request.session["finalize_contact_info"] = {
            "street_address": request.POST.get("street_address"),
            "city": request.POST.get("city"),
            "postal_code": request.POST.get("postal_code"),
            "country": request.POST.get("country"),
            "national_id": request.POST.get("national_id"),
        }

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
        "artwork": bid.artwork,

        # Send saved contact information back to template
        "contact": request.session.get("finalize_contact_info", {})
    })


def payment_details(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Only accepted or contingent bids
    # can continue through finalize flow
    if not can_finalize_bid(bid):

        # Redirect user back to my bids page
        # Optional:
        # Add error message here later if needed
        return redirect("account-bids")

    # If payment details form is submitted
    if request.method == "POST":

        # Save payment information in session
        # so it persists when navigating between finalize steps
        request.session["finalize_payment_info"] = {
            "payment_method": request.POST.get("payment_method"),
            "card_name": request.POST.get("card_name"),
            "card_number": request.POST.get("card_number"),
            "expiry_date": request.POST.get("expiry_date"),
            "cvc": request.POST.get("cvc"),
            "bank_account": request.POST.get("bank_account"),
            "sending_bank": request.POST.get("sending_bank"),
            "routing_number": request.POST.get("routing_number"),
            "account_number": request.POST.get("account_number"),
        }

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
        "artwork": bid.artwork,

        # Send saved payment information back to template
        "payment_info": request.session.get("finalize_payment_info", {})
    })


def review_payment(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Only accepted or contingent bids
    # can continue through finalize flow
    if not can_finalize_bid(bid):

        # Redirect user back to my bids page
        # Optional:
        # Add error message here later if needed
        return redirect("account-bids")

    # Render review page before final confirmation
    return render(request, "payment/review_payment.html", {

        # Send bid to template
        "bid": bid,

        # Send related artwork to template
        "artwork": bid.artwork,

        # Send saved contact information to template
        "contact": request.session.get("finalize_contact_info", {}),

        # Send saved payment information to template
        "payment_info": request.session.get("finalize_payment_info", {}),

        # Hide success modal by default
        "show_success_modal": False
    })


def confirm_payment(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Confirm should only happen through POST
    if request.method != "POST":
        return redirect("review_payment", bid_id=bid.id)

    # Only accepted or contingent bids
    # can continue through finalize flow
    if not can_finalize_bid(bid):

        # Redirect user back to my bids page
        # Optional:
        # Add error message here later if needed
        return redirect("account-bids")

    # Later:
    # Mark bid as paid/finalized

    # Render review page again with success modal open
    return render(request, "payment/review_payment.html", {

        # Send bid to template
        "bid": bid,

        # Send related artwork to template
        "artwork": bid.artwork,

        # Send saved contact information to template
        "contact": request.session.get("finalize_contact_info", {}),

        # Send saved payment information to template
        "payment_info": request.session.get("finalize_payment_info", {}),

        # Open success modal after confirmation
        "show_success_modal": True
    })
