# TODO fara yfir kóða
from django.shortcuts import render, get_object_or_404, redirect

# Import Bid model
from bid.models import Bid

# Import for error messaging
from django.contrib import messages

# Import payments forms
from .forms import  ContactInfoForm,PaymentDetailsForm

# Import payment business logic
from .services import validate_finalize_flow_access

# Import contact info for profile prefill
from user.models import ContactInfo

# Import payment model for database save
from .models import Payment

# TODO
# FINAL VERSION:
# REMOVE:
from django.contrib.auth.models import User
# Add @login_required above this view
# so only authenticated users can finalize bids
#
# Example:
#
# from django.contrib.auth.decorators import login_required
#


def contact_information(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Validate whether bid is allowed
    # to continue through finalize flow
    validation = validate_finalize_flow_access(bid)

    if not validation["is_valid"]:
        # Show validation error message
        messages.error(
            request,
            validation["error"]
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

            # Send bid to template
            "bid": bid,

            # Send related artwork to template
            "artwork": bid.artwork,

            # Send form with validation errors back to template
            "form": form
        })

        # Save validated contact information in session
        # so it persists when navigating between finalize steps
        request.session["finalize_contact_info"] = contact_info

        # Redirect user to payment details step
        return redirect(
            "finalize-payment",
            bid_id=bid.id
        )

    # First use session data if user has already edited checkout contact info
    contact = request.session.get("finalize_contact_info")

    # Check if session contact info contains any actual values
    has_session_contact = contact and any(contact.values())

    if not has_session_contact:

        # TEMPORARY TEST VERSION:
        # Allows finalize flow testing without login
        #
        # TODO FINAL VERSION:
        # Replace this with @login_required
        # and use request.user directly
        if request.user.is_authenticated:
            current_user = request.user
        else:
            current_user = User.objects.get(
                username="User1"
            )

        profile_contact = ContactInfo.objects.filter(
            user=current_user     #TODO change to request.user
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

        # Send bid to template
        "bid": bid,

        # Send related artwork to template
        "artwork": bid.artwork,

        # Send contact form to template
        "form": form
    })


def payment_details(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Validate whether bid is allowed
    # to continue through finalize flow
    validation = validate_finalize_flow_access(bid)

    if not validation["is_valid"]:
        # Show validation error message
        messages.error(
            request,
            validation["error"]
        )

        # Redirect user back to account bids page
        return redirect("account-bids")

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

            # Send bid to template
            "bid": bid,

            # Send related artwork to template
            "artwork": bid.artwork,

            # Send form with errors back to template
            "form": form
        })

        # Create form with saved session data if it exists
        # This keeps payment input values when navigating back
    form = PaymentDetailsForm(
        initial=request.session.get("finalize_payment_info", {})
    )

    # Render payment details page
    return render(request, "payment/payment_details.html", {

        # Send bid to template
        "bid": bid,

        # Send related artwork to template
        "artwork": bid.artwork,

        # Send payment details form to template
        "form": form
    })


def review_payment(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Validate whether bid is allowed
    # to continue through finalize flow
    validation = validate_finalize_flow_access(bid)

    if not validation["is_valid"]:
        # Show validation error message
        messages.error(
            request,
            validation["error"]
        )

        # Redirect user back to account bids page
        return redirect("account-bids")

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

        # Send bid to template
        "bid": bid,

        # Send related artwork to template
        "artwork": bid.artwork,

        # Send saved contact information to template
        "contact": request.session.get("finalize_contact_info", {}),

        # Send saved payment information to template
        "payment_info": request.session.get("finalize_payment_info", {}),

        # Send readable payment method label to template
        "payment_method_label": payment_method_label,

        # Hide success modal by default
        "show_success_modal": False
    })


def confirm_payment(request, bid_id):

    # Get bid by id
    # Return 404 if bid does not exist
    bid = get_object_or_404(Bid, id=bid_id)

    # Validate whether bid is allowed
    # to continue through finalize flow
    validation = validate_finalize_flow_access(bid)

    if not validation["is_valid"]:
        # Show validation error message
        messages.error(
            request,
            validation["error"]
        )

        # Redirect user back to account bids page
        return redirect("account-bids")

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
        user=User.objects.get(username="User1"),            # TODO replace with =request.user
        bid=bid,
        amount=bid.amount,
        payment_method=payment_info["payment_method"],
        status=Payment.STATUS_COMPLETED
    )

    # Mark bid as finalized/completed
    # TODO:
    # Replace STATUS_COMPLETED with the correct Bid status
    # if your Bid model uses a different name
    # bid.status = Bid.STATUS_COMPLETED
    # bid.save()

    # Clear finalize checkout session data
    request.session.pop("finalize_contact_info", None)
    request.session.pop("finalize_payment_info", None)

    # Render review page again with success modal open
    return render(request, "payment/review_payment.html", {
        "bid": bid,
        "artwork": bid.artwork,
        "payment": payment,
        "contact": {},
        "payment_info": payment_info,
        "show_success_modal": True
    })
