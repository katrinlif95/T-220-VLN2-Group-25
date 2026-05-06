from django.http import HttpResponse
from django.shortcuts import render

# dummy data - bráðabirgða, taka út seinna:
artworks = [
    {
        "id": 1,
        "title": "Midnight Dreams",
        "artist": "Anna Jónsdóttir",
        "price": 25000,
        "medium": "Oil",
        "dimensions": "60 x 80 cm",
        "sold": False,
        "image": "images/artworks/art_1.png",
    },
    {
        "id": 2,
        "title": "Golden Silence",
        "artist": "Einar Guðmundsson",
        "price": 45000,
        "medium": "Acrylic",
        "dimensions": "100 x 120 cm",
        "sold": True,
        "image": "images/artworks/art_2.png",
    },
    {
        "id": 3,
        "title": "Northern Lights",
        "artist": "Sara Björk",
        "price": 30000,
        "medium": "Photography",
        "dimensions": "50 x 70 cm",
        "sold": False,
        "image": "images/artworks/art_3.png",
    },
    {
        "id": 4,
        "title": "Abstract Thoughts",
        "artist": "Magnús Karl",
        "price": 20000,
        "medium": "Mixed Media",
        "dimensions": "70 x 70 cm",
        "sold": False,
        "image": "images/artworks/art_4.png",
    },
    {
        "id": 5,
        "title": "Frozen Horizon",
        "artist": "Elín Kristín",
        "price": 38000,
        "medium": "Watercolour",
        "dimensions": "80 x 60 cm",
        "sold": True,
        "image": "images/artworks/art_5.png",
    },
    {
        "id": 6,
        "title": "Silent Echo",
        "artist": "Jón Stefánsson",
        "price": 27000,
        "medium": "Oil",
        "dimensions": "90 x 70 cm",
        "sold": False,
        "image": "images/artworks/art_6.png",
    },
    {
        "id": 7,
        "title": "Crimson Waves",
        "artist": "Kristín María",
        "price": 52000,
        "medium": "Acrylic",
        "dimensions": "120 x 90 cm",
        "sold": True,
        "image": "images/artworks/art_7.png",
    },
    {
        "id": 8,
        "title": "Arctic Bloom",
        "artist": "Björn Einarsson",
        "price": 34000,
        "medium": "Photography",
        "dimensions": "60 x 60 cm",
        "sold": False,
        "image": "images/artworks/art_8.png",
    },
]


def artwork_index(request):
    return render(request, "artwork/artworks.html",{
        # taka næstu línu fyrir neðaan líka út þegar ég tek dummy data í burtu)
        "artworks": artworks
    })

def get_artwork_by_id(request, id):
    return HttpResponse(f"Artwork page: {request.path} with id {id}")

def artwork_detail(request, artwork_id):

    artwork = next(
        (art for art in artworks if art["id"] == artwork_id),
        None
    )

    return render(request, "artwork/artwork_detail.html", {
        "artwork": artwork
    })