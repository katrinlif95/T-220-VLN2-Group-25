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

    return render(request, "artwork/artwork_detail.html", {
        "artwork": artwork,
        "images": images,
        "main_image": main_image,
        "images_data": images_data,
    })