from django.db.models import (
    Exists,
    OuterRef,
    Prefetch,
)
from django.shortcuts import (
    get_object_or_404,
    render,
)

from artwork.models import (
    Artwork,
    ArtworkImage,
)
from bid.models import Bid

from .models import Seller

def artist_index(request):

    # Get all sellers with seller_type = artist
    artists = Seller.objects.filter(
        seller_type="artist"
    )

    # Render artist list page
    return render(request, "seller/artists.html", {
        "artists": artists
    })


def get_artist_by_id(request, seller_id):

    # Get artist by id
    # Return 404 if seller does not exist
    # or if seller is not an artist
    artist = get_object_or_404(
        Seller,
        id=seller_id,
        seller_type="artist"
    )

    # Subquery checking whether each artwork has
    # an accepted or contingent bid
    sold_bid_exists = Bid.objects.filter(
        artwork=OuterRef("pk"),
        status__in=["accepted", "contingent"],
    )

    # Get all artworks listed by this artist
    # Annotate sold status to avoid one query per artwork
    # Prefetch images to avoid one image query per artwork
    artworks = (
        Artwork.objects
        .filter(seller=artist)
        .annotate(
            is_sold=Exists(sold_bid_exists)
        )
        .prefetch_related(
            Prefetch(
                "images",
                queryset=ArtworkImage.objects.order_by("order")
            )
        )
        .order_by("display_order")
    )

    # Send both seller and artworks to the template
    return render(request, "seller/artist_detail.html", {
        "seller": artist,
        "artworks": artworks
    })


def gallery_index(request):

    # Get all sellers with seller_type = gallery
    galleries = Seller.objects.filter(
        seller_type="gallery"
    )

    # Render gallery list page
    return render(request, "seller/galleries.html", {
        "galleries": galleries
    })


def get_gallery_by_id(request, seller_id):

    # Get gallery by id
    # Return 404 if seller does not exist
    # or if seller is not a gallery
    gallery = get_object_or_404(
        Seller,
        id=seller_id,
        seller_type="gallery"
    )

    # Subquery checking whether each artwork has
    # an accepted or contingent bid
    sold_bid_exists = Bid.objects.filter(
        artwork=OuterRef("pk"),
        status__in=["accepted", "contingent"],
    )

    # Get all artworks listed by this gallery
    # Annotate sold status to avoid one query per artwork
    # Prefetch images to avoid one image query per artwork
    artworks = (
        Artwork.objects
        .filter(seller=gallery)
        .annotate(
            is_sold=Exists(sold_bid_exists)
        )
        .prefetch_related(
            Prefetch(
                "images",
                queryset=ArtworkImage.objects.order_by("order")
            )
        )
        .order_by("display_order")
    )

    # Send both seller and artworks to the template
    return render(request, "seller/gallery_detail.html", {
        "seller": gallery,
        "artworks": artworks
    })
