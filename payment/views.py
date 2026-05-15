from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from bid.models import Bid
from django.contrib import messages
from .forms import  ContactInfoForm,PaymentDetailsForm
from .services import validate_finalize_flow_access, reject_other_pending_bids
from user.models import ContactInfo
from .models import Payment


# Build context values used by the checkout step navigation
def get_checkout_navigation_context(request):
    return {
        "can_go_to_payment": "finalize_contact_info" in request.session,
        "can_go_to_review": (
            "finalize_contact_info" in request.session
            and "finalize_payment_info" in request.session
        )
    }

# Display and save contact information for the finalize checkout flow
@login_required
def contact_information(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Validate that the current user owns the bid
    # and that the bid can be finalized
    validation = validate_finalize_flow_access(
        bid,
        request.user
    )

    if not validation["is_valid"]:
        # Show validation error message
        messages.error(
            request,
            validation["error"],
            extra_tags = "finalize"
        )

        # Redirect user back to account bids page
        return redirect("account-bids")

    # If contact information form is submitted
    if request.method == "POST":

        # Create form instance with submitted contact information
        form = ContactInfoForm(request.POST)

        # If form is valid, save cleaned contact info in session
        if form.is_valid():
            request.session["finalize_contact_info"] = form.cleaned_data

            # Redirect user to payment details step
            return redirect(
                "finalize-payment",
                bid_id=bid.id
            )

        # If form is invalid,
        # re-render contact information page with validation errors
        return render(request, "payment/contact_information.html", {
            "bid": bid,
            "artwork": bid.artwork,
            "form": form,

            "current_step": "contact",

            **get_checkout_navigation_context(request),
        })

    # First use session data if user has already edited checkout contact info
    contact = request.session.get("finalize_contact_info")

    # Check if session contact info contains any actual values
    has_session_contact = contact and any(contact.values())

    if not has_session_contact:

        profile_contact = ContactInfo.objects.filter(
            user=request.user
        ).first()

        # If profile contact info exists,
        # convert it to the same format used by the checkout form
        if profile_contact:
            contact = {
                "street_address": profile_contact.street_address,
                "city": profile_contact.city,
                "postal_code": profile_contact.postal_code,
                "country": profile_contact.country,
                "national_id": profile_contact.national_id,
            }

        # If no profile contact info exists,
        # use an empty dictionary so the form is empty
        else:
            contact = {}

    # Create form with existing contact information
    # from session, profile prefill, or empty values
    form = ContactInfoForm(initial=contact)

    # Render contact information page
    return render(request, "payment/contact_information.html", {

        "bid": bid,
        "artwork": bid.artwork,
        "form": form,

        "current_step": "contact",

        ** get_checkout_navigation_context(request),
    })

# Display and save payment details for the finalize checkout flow
@login_required
def payment_details(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Validate that the current user owns the bid
    # and that the bid can be finalized
    validation = validate_finalize_flow_access(
        bid,
        request.user
    )

    if not validation["is_valid"]:
        # Show validation error message
        messages.error(
            request,
            validation["error"],
            extra_tags = "finalize"
        )

        # Redirect user back to account bids page
        return redirect("account-bids")

    # User must complete contact information
    # before accessing payment details
    if "finalize_contact_info" not in request.session:
        return redirect(
            "finalize-contact",
            bid_id=bid.id
        )

    # If payment details form is submitted
    if request.method == "POST":

        # Create form instance with submitted payment data
        form = PaymentDetailsForm(request.POST)

        # If form is valid, save cleaned payment info in session
        if form.is_valid():
            request.session["finalize_payment_info"] = form.cleaned_data

            # Redirect user to review step
            return redirect(
                "finalize-review",
                bid_id=bid.id
            )

        # If form is invalid,
        # re-render payment details page with validation errors
        return render(request, "payment/payment_details.html", {
            "bid": bid,
            "artwork": bid.artwork,
            "form": form,

            "current_step": "payment",

            **get_checkout_navigation_context(request),
        })

        # Create form with saved session data if it exists
        # This keeps payment input values when navigating back
    form = PaymentDetailsForm(
        initial=request.session.get("finalize_payment_info", {})
    )

    # Render payment details page
    return render(request, "payment/payment_details.html", {
        "bid": bid,
        "artwork": bid.artwork,
        "form": form,

        "current_step": "payment",

        **get_checkout_navigation_context(request),
    })

# Display a review page before the user confirms payment
@login_required
def review_payment(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Validate that the current user owns the bid
    # and that the bid can be finalized
    validation = validate_finalize_flow_access(
        bid,
        request.user
    )

    if not validation["is_valid"]:
        # Show validation error message
        messages.error(
            request,
            validation["error"],
            extra_tags = "finalize"
        )

        # Redirect user back to account bids page
        return redirect("account-bids")

    # User must complete contact information
    # before accessing review
    if "finalize_contact_info" not in request.session:
        return redirect(
            "finalize-contact",
            bid_id=bid.id
        )

    # User must complete payment details
    # before accessing review
    if "finalize_payment_info" not in request.session:
        return redirect(
            "finalize-payment",
            bid_id=bid.id
        )

    # Get saved payment information from session
    payment_info = request.session.get(
        "finalize_payment_info",
        {}
    )

    # Convert payment method database/session value
    # into a readable label for the template
    payment_method_labels = {
        "credit_card": "Credit card",
        "bank_transfer": "Bank transfer",
        "wire_transfer": "Wire transfer",
    }

    # Get readable payment method label
    # Example: "bank_transfer" becomes "Bank transfer"
    payment_method_label = payment_method_labels.get(
        payment_info.get("payment_method"),
        ""
    )

    # Render review page before final confirmation
    return render(request, "payment/review_payment.html", {
        "bid": bid,
        "artwork": bid.artwork,
        "contact": request.session.get("finalize_contact_info", {}),
        "payment_info": request.session.get("finalize_payment_info", {}),
        "payment_method_label": payment_method_label,
        "show_success_modal": False,

        "current_step": "review",

        ** get_checkout_navigation_context(request),
    })

# Create the payment record and show the success confirmation modal
@login_required
def confirm_payment(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Validate that the current user owns the bid
    # and that the bid can be finalized
    validation = validate_finalize_flow_access(
        bid,
        request.user
    )

    if not validation["is_valid"]:
        # Show validation error message
        messages.error(
            request,
            validation["error"],
            extra_tags = "finalize"
        )

        # Redirect user back to account bids page
        return redirect("account-bids")

    # User must complete contact information
    # before confirming payment
    if "finalize_contact_info" not in request.session:
        return redirect(
            "finalize-contact",
            bid_id=bid.id
        )

    # Get saved payment information from session
    payment_info = request.session.get("finalize_payment_info")

    # If payment information is missing,
    # send user back to payment details step
    if not payment_info:
        return redirect(
            "finalize-payment",
            bid_id=bid.id
        )

    # Create payment record in database
    payment = Payment.objects.create(
        user=request.user,
        bid=bid,
        amount=bid.amount,
        payment_method=payment_info["payment_method"],
        status=Payment.STATUS_COMPLETED
    )

    # Reject all other pending bids
    # on the same artwork after successful payment
    reject_other_pending_bids(bid)

    # Clear finalize checkout session data
    request.session.pop("finalize_contact_info", None)
    request.session.pop("finalize_payment_info", None)

    # Convert payment method value into readable label
    payment_method_labels = {
        "credit_card": "Credit card",
        "bank_transfer": "Bank transfer",
        "wire_transfer": "Wire transfer",
    }

    payment_method_label = payment_method_labels.get(
        payment_info.get("payment_method"),
        ""
    )

    # Render review page again with success modal open
    return render(request, "payment/review_payment.html", {
        "bid": bid,
        "artwork": bid.artwork,
        "payment": payment,
        "contact": {},
        "payment_info": payment_info,
        "payment_method_label": payment_method_label,

        "current_step": "review",

        **get_checkout_navigation_context(request),

        "show_success_modal": True,
        "user": request.user,
    })
