from django.db.models import Min, Max
from django.shortcuts import render, get_object_or_404
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING

from artwork.models import Artwork
from artwork.services import (
    add_artwork_display_status,
    artwork_is_sold,
    get_current_highest_bid_amount,
)

from bid.forms import BidForm
from bid.models import Bid

import math

def artwork_index(request):

    # Get all artworks before filtering
    artworks = Artwork.objects.all()

    # Get selected filter values from URL query parameters
    selected_status = request.GET.get("status", "")
    selected_medium = request.GET.get("medium", "")
    selected_style = request.GET.get("style", "")
    selected_order_by = request.GET.get("order_by", "")
    search_query = request.GET.get("search", "")
    highlighted_only = request.GET.get("highlighted") == "true"
    selected_artist = request.GET.get("artist", "")

    # Price slider step size
    # Used for rounded slider increments
    price_step = Decimal("10000")

    # Calculate lowest and highest starting price
    # from all artworks in the database
    price_range = Artwork.objects.aggregate(
        lowest_price=Min("starting_price"),
        highest_price=Max("starting_price")
    )

    # Fallback to 0 if database is empty
    lowest_price = (
        price_range["lowest_price"]
        or Decimal("0")
    )

    highest_price = (
        price_range["highest_price"]
        or Decimal("0")
    )

    # Round slider minimum DOWN
    # to nearest 10.000
    slider_min_price = (
        (lowest_price / price_step)
        .to_integral_value(
            rounding=ROUND_FLOOR
        )
        * price_step
    )

    # Round slider maximum UP
    # to nearest 10.000
    slider_max_price = (
        (highest_price / price_step)
        .to_integral_value(
            rounding=ROUND_CEILING
        )
        * price_step
    )

    # Check whether price filter is active
    price_filter_active = (
        "min_price" in request.GET
        or "max_price" in request.GET
    )

    # Get selected min/max prices from sliders
    # If no filter is active, use full slider range
    selected_min_price = request.GET.get(
        "min_price",
        slider_min_price
    )

    selected_max_price = request.GET.get(
        "max_price",
        slider_max_price
    )

    # Filter by artwork status
    if selected_status:
        artworks = artworks.filter(
            status=selected_status
        )

    # Filter by medium
    if selected_medium:
        artworks = artworks.filter(
            medium__iexact=selected_medium
        )

    # Filter by style
    if selected_style:
        artworks = artworks.filter(
            style__iexact=selected_style
        )

    # Search by artwork title
    # Requirement: case-insensitive title search
    if search_query:
        artworks = artworks.filter(
            title__icontains=search_query
        )

    # Filter by selected price range
    if price_filter_active:
        artworks = artworks.filter(
            starting_price__gte=selected_min_price,
            starting_price__lte=selected_max_price
        )

    # Order by selected sorting option
    if selected_order_by == "title-asc":
        artworks = artworks.order_by("title")

    elif selected_order_by == "title-desc":
        artworks = artworks.order_by("-title")

    elif selected_order_by == "price-asc":
        artworks = artworks.order_by(
            "starting_price"
        )

    elif selected_order_by == "price-desc":
        artworks = artworks.order_by(
            "-starting_price"
        )

    # Default artwork ordering
    else:
        artworks = artworks.order_by(
            "display_order"
        )

    # Add display status, e.g. sold / available
    artworks = add_artwork_display_status(
        artworks
    )

    if highlighted_only:
        artworks = artworks.filter(
            highlighted=True
        )

    if selected_artist:
        artworks = artworks.filter(
            artist_name__iexact=selected_artist
        )

    return render(
        request,
        "artwork/artworks.html",
        {
            "artworks": artworks,

            "selected_status": selected_status,
            "selected_medium": selected_medium,
            "selected_style": selected_style,
            "selected_order_by": selected_order_by,
            "search_query": search_query,

            "price_filter_active": price_filter_active,

            "lowest_price": lowest_price,
            "highest_price": highest_price,

            "slider_min_price": slider_min_price,
            "slider_max_price": slider_max_price,

            "price_step": price_step,

            "selected_min_price": selected_min_price,
            "selected_max_price": selected_max_price,

            "highlighted_only": highlighted_only,
            "selected_artist": selected_artist,
        }
    )


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

    # Check whether logged-in user already has a bid
    # that can be resubmitted on this artwork
    existing_resubmittable_bid = None

    if request.user.is_authenticated:
        existing_resubmittable_bid = Bid.objects.filter(
            user=request.user,
            artwork=artwork,
            status__in=[
                Bid.STATUS_PENDING,
                Bid.STATUS_REJECTED,
            ]
        ).first()

    # Create empty bid form for submit bid modal
    bid_form = BidForm()

    return render(request, "artwork/artwork_detail.html", {
        "artwork": artwork,
        "images": images,
        "main_image": main_image,
        "images_data": images_data,
        "is_sold": is_sold,
        "highest_bid_amount": get_current_highest_bid_amount(artwork),
        "existing_resubmittable_bid": existing_resubmittable_bid,
        "bid_form": bid_form,
    })