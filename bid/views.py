from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from artwork.models import Artwork
from artwork.services import artwork_is_sold, get_current_highest_bid_amount

from .forms import BidForm
from .models import Bid


# Only logged-in users can submit bids
@login_required
def submit_bid(request, artwork_id):

    # Get artwork by id
    # Return 404 if artwork does not exist
    artwork = get_object_or_404(
        Artwork,
        id=artwork_id
    )

    # Prevent bidding on sold artworks
    if artwork_is_sold(artwork):
        return redirect(
            "artwork-detail",
            artwork_id=artwork.id
        )

    # Handle submitted bid form
    if request.method == "POST":

        # Check whether user already has
        # a pending bid on this artwork
        existing_pending_bid = Bid.objects.filter(
            user=request.user,
            artwork=artwork,
            status=Bid.STATUS_PENDING
        ).first()

        # Populate form with submitted POST data
        # and provide related artwork/existing bid
        # for validation
        form = BidForm(
            request.POST,
            artwork=artwork,
            existing_bid=existing_pending_bid
        )

        # Run form + model validation
        if form.is_valid():

            # Check whether user already has
            # a pending bid on this artwork
            existing_pending_bid = Bid.objects.filter(
                user=request.user,
                artwork=artwork,
                status=Bid.STATUS_PENDING
            ).first()

            # Create bid object without saving yet
            # Needed to manually assign user/artwork
            bid = form.save(commit=False)

            # Update existing pending bid
            # instead of creating a new one
            if existing_pending_bid:

                existing_pending_bid.amount = bid.amount
                existing_pending_bid.expires_at = bid.expires_at

                existing_pending_bid.save()

            # Otherwise create a completely new bid
            else:
                bid.user = request.user
                bid.artwork = artwork
                bid.status = Bid.STATUS_PENDING

                bid.save()
        else:
            # Re-render artwork detail page with
            # form errors visible in the bid modal
            images = artwork.images.order_by("order")
            main_image = images.first()

            images_data = [
                {
                    "url": image.image_url,
                    "alt": image.alt_text,
                }
                for image in images
            ]

            return render(request, "artwork/artwork_detail.html", {
                "artwork": artwork,
                "images": images,
                "main_image": main_image,
                "images_data": images_data,
                "is_sold": artwork_is_sold(artwork),
                "highest_bid_amount": get_current_highest_bid_amount(artwork),
                "existing_pending_bid": existing_pending_bid,
                "bid_form": form,
                "open_bid_modal": True,
            })

    # Redirect back to artwork detail page
    return redirect(
        "artwork-detail",
        artwork_id=artwork.id
    )