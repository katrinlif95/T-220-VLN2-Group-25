from django.shortcuts import render, get_object_or_404

from artwork.models import Artwork


def artwork_index(request):

    artworks = Artwork.objects.all().order_by("display_order")

    return render(request, "artwork/artworks.html", {
        "artworks": artworks,
    })


def artwork_detail(request, artwork_id):

    artwork = get_object_or_404(
        Artwork,
        id=artwork_id
    )

    return render(request, "artwork/artwork_detail.html", {
        "artwork": artwork,
    })