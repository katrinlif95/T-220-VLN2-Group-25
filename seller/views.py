from django.shortcuts import render, get_object_or_404

from .models import Seller

from artwork.models import Artwork


# Dummy data hér fyrir neðan:
sellers = [
{
    "id": 1,
    "display_name": "Atelier V",
    "type": "Gallery",
    "street_name": "Laugavegur 12, 101 Reykjavík",
    "opening_hours": "Mon–Fri: 10:00–18:00",
    "email": "info@atelierv.is",
    "logo_url": "images/galleries/atelier_v/gallery_1_logo.png",
    "cover_image_url": "images/galleries/atelier_v/gallery_1_banner.png",
    "bio": "Atelier V is a contemporary art gallery dedicated to showcasing bold and expressive works by emerging and established artists. The gallery focuses on abstraction, color, and modern visual culture."
},

{
    "id": 2,
    "display_name": "Obsidian Gallery",
    "type": "Gallery",
    "street_name": "Skólavörðustígur 7, 101 Reykjavík",
    "opening_hours": "Mon–Fri: 10:00–18:00",
    "email": "contact@obsidiangallery.is",
    "logo_url": "images/galleries/obsidian_gallery/obsidian_gallery_logo.png",
    "cover_image_url": "images/galleries/obsidian_gallery/obsidian_gallery_cover.png",
    "bio": "Obsidian Gallery curates atmospheric contemporary works including minimalist sculpture, dramatic landscapes, photography, and modern abstract art."
},

{
    "id": 3,
    "display_name": "Adrian Sol",
    "type": "Artist",
    "email": "studio@adriansol.com",
    "logo_url": "images/artists/adrian_sol/adrian_sol_logo.png",
    "cover_image_url": "images/artists/adrian_sol/adrian_sol_cover.png",
    "bio": "Adrian Sol creates geometric sculptural compositions inspired by balance, architecture, and material form. His work explores the relationship between symmetry and space."
},

{
    "id": 4,
    "display_name": "Camille Laurent",
    "type": "Artist",
    "email": "studio@camillelaurent.com",
    "logo_url": "images/artists/camille_laurent/camille_laurent_logo.png",
    "cover_image_url": "images/artists/camille_laurent/camille_laurent_cover.png",
    "bio": "Camille Laurent is known for expressive floral still life paintings with layered textures and soft impressionistic color palettes."
},

{
    "id": 5,
    "display_name": "Isabella Moreau",
    "type": "Individual",
    "email": "hello@isabellamoreau.com",
    "logo_url": "images/sellers/isabella_moreau_logo.png",
    "cover_image_url": "images/sellers/isabella_moreau_cover.png",
    "bio": "Isabella Moreau paints serene Mediterranean-inspired architectural scenes that combine warm light, coastal landscapes, and minimalist compositions."
},

{
    "id": 6,
    "display_name": "Lucien Vale",
    "type": "Individual",
    "email": "contact@lucienvale.com",
    "logo_url": "images/sellers/lucien_vale_logo.png",
    "cover_image_url": "images/sellers/lucien_vale_cover.png",
    "bio": "Lucien Vale is a portrait artist exploring identity and emotion through expressive color, layered brushwork, and dramatic contrast."
}

]


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


def get_gallery_by_id(request, seller_id):

    # Get gallery by id
    # Return 404 if seller does not exist
    # or if seller is not a gallery
    gallery = get_object_or_404(
        Seller,
        id=seller_id,
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

# Hér fyrir neðan er allt fyrir dummy data, tek út þegar gagnagrunnur er klár:
def gallery_index_dummy(request):
    galleries = [
        seller for seller in sellers
        if seller.get("type") == "Gallery"
    ]
    #print("GALLERIES:", galleries)
    return render(request, "seller/galleries.html", {
        "sellers": galleries,
    })


def gallery_detail_dummy(request, seller_id):
    seller = next(
        (seller for seller in sellers if seller["id"] == seller_id),
        None
    )

    seller_artworks = [
        artwork for artwork in artworks
        if artwork["seller"] == seller["display_name"]
    ]

    return render(request, "seller/gallery_detail.html", {
        "seller": seller,
        "seller_artworks": seller_artworks,
    })

def artist_index_dummy(request):
    artists = [
        seller for seller in sellers
        if seller.get("type") == "Artist"
    ]

    #print("Artists", artists)
    return render(request, "seller/artists.html", {
        "artists": artists,
    })

def artist_detail_dummy(request, seller_id):
    artist = next(
        (seller for seller in sellers if seller["id"] == seller_id),
        None
    )

    artist_artworks = [
        artwork for artwork in artworks
        if artwork["seller"] == artist["display_name"]
    ]

    return render(request, "seller/artist_detail.html", {
        "artist": artist,
        "artist_artworks": artist_artworks,
    })
