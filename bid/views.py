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

        # Check whether user already has a bid
        # that can be resubmitted on this artwork
        existing_resubmittable_bid = Bid.objects.filter(
            user=request.user,
            artwork=artwork,
            status__in=[
                Bid.STATUS_PENDING,
                Bid.STATUS_REJECTED,
            ]
        ).first()

        form = BidForm(
            request.POST,
            artwork=artwork,
            existing_bid=existing_resubmittable_bid
        )

        # Run form + model validation
        if form.is_valid():

            bid = form.save(commit=False)

            # Update existing pending/rejected bid
            # instead of creating a new one
            if existing_resubmittable_bid:

                existing_resubmittable_bid.amount = bid.amount
                existing_resubmittable_bid.expires_at = bid.expires_at

                # If the bid was rejected, resubmitting it
                # should make it pending again
                existing_resubmittable_bid.status = Bid.STATUS_PENDING

                existing_resubmittable_bid.save()

                messages.success(
                    request,
                    "Bid resubmitted successfully."
                )



            # Otherwise create a completely new bid
            else:
                bid.user = request.user
                bid.artwork = artwork
                bid.status = Bid.STATUS_PENDING

                bid.save()

                messages.success(
                    request,
                    "Bid submitted successfully."
                )

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
                "existing_resubmittable_bid": existing_resubmittable_bid,
                "bid_form": form,
                "open_bid_modal": True,
            })

    # Redirect back to artwork detail page
    return redirect(
        "artwork-detail",
        artwork_id=artwork.id
    )