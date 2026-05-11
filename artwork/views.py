from django.shortcuts import render, get_object_or_404
from artwork.models import Artwork
from artwork.services import add_artwork_display_status, artwork_is_sold, get_current_highest_bid_amount
from bid.forms import BidForm
from bid.models import Bid

def artwork_index(request):

    artworks = Artwork.objects.all().order_by(
        "display_order"
    )

    artworks = add_artwork_display_status(
        artworks
    )

    return render(request, "artwork/artworks.html", {
        "artworks": artworks,
    })


def artwork_detail(request, artwork_id):

    artwork = get_object_or_404(
        Artwork,
        id=artwork_id
    )

    # Get artwork images in display order
    images = artwork.images.order_by("order")
    # Set first image as the main displayed image
    main_image = images.first()

    # Prepare image data for JavaScript carousel functionality
    images_data = [
        {
            "url": image.image_url,
            "alt": image.alt_text,
        }
        for image in images
    ]

    # Check if artwork should be displayed as sold
    is_sold = artwork_is_sold(artwork)

    # Get highest actual bid amount, if any
    highest_bid_amount = get_current_highest_bid_amount(artwork)

    # Check whether logged-in user already has a pending bid on this artwork
    existing_pending_bid = None

    if request.user.is_authenticated:
        existing_pending_bid = Bid.objects.filter(
            user=request.user,
            artwork=artwork,
            status=Bid.STATUS_PENDING
        ).first()

    # Create empty bid form for submit bid modal
    bid_form = BidForm()

    return render(request, "artwork/artwork_detail.html", {
        "artwork": artwork,
        "images": images,
        "main_image": main_image,
        "images_data": images_data,
        "is_sold": is_sold,
        "highest_bid_amount": highest_bid_amount,
        "existing_pending_bid": existing_pending_bid,
        "bid_form": bid_form,
    })