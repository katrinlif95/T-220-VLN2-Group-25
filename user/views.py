from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from bid.models import Bid

from artwork.services import get_current_highest_bid_amount

from .forms import ProfileUpdateForm, ContactInfoProfileForm
from .models import (
    ContactInfo,
    UserProfile,
)

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