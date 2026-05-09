from django.shortcuts import render, redirect

# Create your views here.
from bid.models import Bid
from django.contrib.auth.models import User  #má taka út þegar login flow er orðið virkt og hardcoded test búið
from .models import ContactInfo

# Main account/profile page
# Displays general user profile information
def profile_detail(request):

    return render(
        request,
        "user/profile.html"
    )


# Page showing all bids belonging to the logged-in user
def account_bids(request):

    # Clear finalize checkout session data
    # when user returns to the account bids page
    request.session.pop("finalize_contact_info", None)
    request.session.pop("finalize_payment_info", None)


    # TODO FINAL VERSION : Get all bids belonging to current logged-in user
    # bids = Bid.objects.filter(
        #user=request.user
    #)


    # TEMPORARY TEST VERSION: (svo það þurfi ekki að vera logged in til að sjá bids)
    # Manually fetch a specific test user from database
    test_user = User.objects.get(
        username="ernao"
    )

    # Get bids belonging to test user
    bids = Bid.objects.filter(
        user=test_user
    )

    # Mark bids that already have completed payments
    for bid in bids:
        bid.is_finalized = bid.payments.filter(
            status="completed"
        ).exists()

    return render(
        request,
        "user/bids.html",
        {
            "bids": bids
        }
    )


# Page for viewing and editing user contact information
def contact_information(request):

    # Try to get contact information for the logged-in user.
    # If no contact info exists yet, contact will be None.
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