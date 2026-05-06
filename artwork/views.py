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
        "image": "images/art1.jpg",
    },
    {
        "id": 2,
        "title": "Golden Silence",
        "artist": "Einar Guðmundsson",
        "price": 45000,
        "medium": "Acrylic",
        "dimensions": "100 x 120 cm",
        "sold": True,
        "image": "images/art2.jpg",
    },
    {
        "id": 3,
        "title": "Northern Lights",
        "artist": "Sara Björk",
        "price": 30000,
        "medium": "Photography",
        "dimensions": "50 x 70 cm",
        "sold": False,
        "image": "images/art3.jpg",
    },
    {
        "id": 4,
        "title": "Abstract Thoughts",
        "artist": "Magnús Karl",
        "price": 20000,
        "medium": "Mixed Media",
        "dimensions": "70 x 70 cm",
        "sold": False,
        "image": "images/art4.jpg",
    },
    {
        "id": 5,
        "title": "Frozen Horizon",
        "artist": "Elín Kristín",
        "price": 38000,
        "medium": "Watercolour",
        "dimensions": "80 x 60 cm",
        "sold": True,
        "image": "images/art5.jpg",
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