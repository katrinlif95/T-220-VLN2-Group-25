from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from bid.models import Bid
from bid.services import mark_bid_as_expired
from django.db.models import Exists, OuterRef, Subquery
from payment.models import Payment


from .forms import ProfileUpdateForm, ContactInfoProfileForm
from .models import (
    ContactInfo,
    UserProfile,
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

# Main account/profile page
# Displays general user profile information
@login_required
def profile_detail(request):

    # Get or create profile connected to current user
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    # Handle submitted profile update form
    if request.method == "POST":

        # Bind submitted form data and uploaded files
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
        )

        # Validate submitted form data
        if form.is_valid():

            # Update Django User model fields
            request.user.first_name = form.cleaned_data["first_name"]
            request.user.last_name = form.cleaned_data["last_name"]

            # Save updated user information
            request.user.save()

            # Update uploaded profile image if provided
            if form.cleaned_data["profile_image"]:
                profile.profile_image = form.cleaned_data["profile_image"]

                # Save updated profile image
                profile.save()

            # Success confirmation message
            messages.success(
                request,
                "Profile updated successfully."
            )

            # Redirect back to profile page
            return redirect("account-profile")

        # Error message shown if form validation fails
        messages.error(
            request,
            "Failed to update profile."
        )

    else:

        # Prefill form with current user information
        form = ProfileUpdateForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            }
        )

    # Render profile page with form and profile data
    return render(
        request,
        "user/profile.html",
        {
            "form": form,
            "profile": profile,
        }
    )

# Page showing all bids belonging to the logged-in user
@login_required
def account_bids(request):

    # Clear finalize checkout session data
    # when user returns to the account bids page
    request.session.pop("finalize_contact_info", None)
    request.session.pop("finalize_payment_info", None)

    # Subquery checking whether each bid
    # already has a completed payment
    completed_payment_exists = Payment.objects.filter(
        bid=OuterRef("pk"),
        status="completed",
    )

    # Subquery getting the highest active bid
    # amount for the same artwork as this bid
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

    # Get bids belonging to current logged-in user
    # select_related loads artwork and seller in the same query
    # prefetch_related loads artwork images in one extra query
    # annotate adds is_finalized without one payment query per bid
    bids = (
        Bid.objects
        .filter(user=request.user)
        .select_related(
            "artwork",
            "artwork__seller",
        )
        .prefetch_related(
            "artwork__images",
        )
        .annotate(
            is_finalized=Exists(completed_payment_exists),
            artwork_annotated_highest_bid_amount=Subquery(
                highest_bid_amount
            ),
        )
    )

    # Update pending bids to expired
    # if their expiration date has passed
    for bid in bids:
        mark_bid_as_expired(bid)

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

        # Bind submitted data to ContactInfoProfileForm
        form = ContactInfoProfileForm(
            request.POST,
            instance=contact
        )

        # Validate submitted contact information
        if form.is_valid():

            # Create/update contact object, but do not save yet
            contact = form.save(commit=False)

            # Make sure contact info belongs to current user
            contact.user = request.user

            # Save contact info to database
            contact.save()

            messages.success(
                request,
                "Contact information updated successfully."
            )

            # Redirect to prevent duplicate form submission
            return redirect("account-contact")

        messages.error(
            request,
            "Failed to update contact information."
        )

    else:

        # Prefill form with existing contact information
        form = ContactInfoProfileForm(
            instance=contact
        )

    return render(
        request,
        "user/contact_information.html",
        {
            "contact": contact,
            "form": form,
        }
    )