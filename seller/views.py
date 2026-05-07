from django.shortcuts import render, get_object_or_404

from .models import Seller
from artwork.models import Artwork


def artist_index(request):

    # Get all sellers with seller_type = artist
    artists = Seller.objects.filter(
        seller_type="artist"
    )

    # Render artist list page
    return render(request, "seller/artists.html", {
        "artists": artists
    })


def get_artist_by_id(request, id):

    # Get artist by id
    # Return 404 if seller does not exist
    # or if seller is not an artist
    artist = get_object_or_404(
        Seller,
        id=id,
        seller_type="artist"
    )

    # Get all artworks listed by this artist
    artworks = Artwork.objects.filter(
        seller=artist
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


def get_gallery_by_id(request, id):

    # Get gallery by id
    # Return 404 if seller does not exist
    # or if seller is not a gallery
    gallery = get_object_or_404(
        Seller,
        id=id,
        seller_type="gallery"
    )

    # Get all artworks listed by this gallery
    artworks = Artwork.objects.filter(
        seller=gallery
    )

    # Send both seller and artworks to the template
    return render(request, "seller/gallery_detail.html", {
        "seller": gallery,
        "artworks": artworks
    })