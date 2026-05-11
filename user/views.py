from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from bid.models import Bid
from .models import ContactInfo
from artwork.services import get_current_highest_bid_amount

# Main account/profile page
# Displays general user profile information
@login_required
def profile_detail(request):

    return render(
        request,
        "user/profile.html"
    )

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "user/register.html", {
        'form': form
    })

# Page showing all bids belonging to the logged-in user
@login_required
def account_bids(request):

    # Clear finalize checkout session data
    # when user returns to the account bids page
    request.session.pop("finalize_contact_info", None)
    request.session.pop("finalize_payment_info", None)


    # Get bids belonging to current logged-in user
    bids = Bid.objects.filter(
        user=request.user
    )

    # Add extra display information to each bid
    for bid in bids:
        # Mark bids that already have
        # a completed payment
        bid.is_finalized = bid.payments.filter(
            status="completed"
        ).exists()

        # Add current highest bid amount
        # for artwork display
        bid.artwork.highest_bid_amount = (
            get_current_highest_bid_amount(
                bid.artwork
            )
        )
    return render(
        request,
        "user/bids.html",
        {
            "bids": bids
        }
    )


# Page for viewing and editing user contact information
@login_required
def contact_information(request):

    # Get contact information belonging to current logged-in user
    contact = ContactInfo.objects.filter(
        user=request.user
    ).first()

    # If contact information form is submitted
    if request.method == "POST":

        # If contact info does not exist yet,
        # create a new ContactInfo object for this user
        if contact is None:
            contact = ContactInfo(
                user=request.user
            )

        # Update contact info fields from submitted form data
        contact.street_address = request.POST.get("street_address")
        contact.city = request.POST.get("city")
        contact.postal_code = request.POST.get("postal_code")
        contact.country = request.POST.get("country")
        contact.national_id = request.POST.get("national_id")

        # Save contact info to database
        contact.save()

        # Redirect back to contact information page
        # to prevent duplicate form submission on refresh
        return redirect("account-contact")

    return render(
        request,
        "user/contact_information.html",
        {
            "contact": contact
        }
    )