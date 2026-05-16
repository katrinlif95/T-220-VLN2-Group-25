from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import (
    Case,
    Exists,
    F,
    IntegerField,
    OuterRef,
    Prefetch,
    Subquery,
    Value,
    When,
)
from django.shortcuts import redirect, render
from django.utils import timezone

from artwork.models import ArtworkImage
from bid.models import Bid
from bid.services import get_bid_alert_counts
from payment.models import Payment

from .forms import (
    ContactInfoProfileForm,
    ProfileUpdateForm,
)
from .models import (
    ContactInfo,
    UserProfile,
)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect("account-profile")

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

    # Get bid alert counts for profile messages
    bid_alert_counts = get_bid_alert_counts(request.user)

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

        # Get bid alert counts shown on profile/account pages
        bid_alert_counts = get_bid_alert_counts(
            request.user
        )

    # Render profile page with form and profile data
    return render(
        request,
        "user/profile.html",
        {
            "form": form,
            "profile": profile,
            "bid_alert_counts": bid_alert_counts,
        }
    )

# Page showing all bids belonging to the logged-in user
@login_required
def account_bids(request):
    # Clear finalize checkout session data
    # when user returns to the account bids page
    request.session.pop("finalize_contact_info", None)
    request.session.pop("finalize_payment_info", None)

    # Get selected filter from URL
    selected_filter = request.GET.get("filter", "all")

    # Get artwork ids where current user has placed bids
    user_artwork_ids = Bid.objects.filter(
        user=request.user
    ).values_list(
        "artwork_id",
        flat=True
    )

    # Expire all pending bids on those artworks
    # if their expiration time has passed
    Bid.objects.filter(
        artwork_id__in=user_artwork_ids,
        status="pending",
        expires_at__lt=timezone.now(),
    ).update(
        status="expired"
    )

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
    bids = (
        Bid.objects
        .filter(user=request.user)
        .select_related(
            "artwork",
            "artwork__seller",
        )
        .prefetch_related(
            Prefetch(
                "artwork__images",
                queryset=ArtworkImage.objects.order_by("order"),
                to_attr="ordered_images",
            )
        )
        .annotate(
            is_finalized=Exists(completed_payment_exists),
            artwork_annotated_highest_bid_amount=Subquery(
                highest_bid_amount
            ),
            sort_order=Case(
                # Accepted / contingent bids
                # that still need to be finalized
                When(
                    status__in=[
                        "accepted",
                        "contingent",
                    ],
                    is_finalized=False,
                    then=Value(1),
                ),

                # Pending bids
                When(
                    status="pending",
                    then=Value(2),
                ),

                # Rejected bids
                When(
                    status="rejected",
                    then=Value(3),
                ),

                # Expired bids
                When(
                    status="expired",
                    then=Value(4),
                ),

                # Finalized bids
                When(
                    is_finalized=True,
                    then=Value(5),
                ),

                # Fallback for any other status
                default=Value(6),
                output_field=IntegerField(),
            ),
        )
    )

    # Apply selected filter
    if selected_filter == "pending":
        bids = bids.filter(
            status="pending"
        )

    elif selected_filter == "outbid":
        bids = bids.filter(
            status="pending",
            amount__lt=F("artwork_annotated_highest_bid_amount"),
        )

    elif selected_filter == "contingent":
        bids = bids.filter(
            status="contingent"
        )

    elif selected_filter == "accepted":
        bids = bids.filter(
            status="accepted"
        )

    elif selected_filter == "finalized":
        bids = bids.filter(
            is_finalized=True
        )

    elif selected_filter == "rejected":
        bids = bids.filter(
            status="rejected"
        )

    elif selected_filter == "expired":
        bids = bids.filter(
            status="expired"
        )

    elif selected_filter == "unpaid":
        bids = bids.filter(
            status__in=[
                "accepted",
                "contingent",
            ],
            is_finalized=False,
        )

    # Order bids after filters have been applied
    bids = bids.order_by(
        "sort_order",
        "-created_at",
    )

    # Get bid alert counts shown on profile/account pages
    bid_alert_counts = get_bid_alert_counts(
        request.user
    )

    return render(
        request,
        "user/bids.html",
        {
            "bids": bids,
            "bid_alert_counts": bid_alert_counts,
            "selected_filter": selected_filter,
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