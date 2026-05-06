from django.http import HttpResponse
from django.shortcuts import render

# dummy data
artworks = [
    {
        "id": 1,
        "title": "Solitude Horizon",
        "artist": "Elías Jónsson",
        "seller": "North Contemporary",
        "seller_description": "Contemporary gallery specializing in atmospheric Nordic-inspired and nature-focused works.",
        "medium": "Oil on canvas",
        "style": "Contemporary minimalism",
        "dimensions": "100 × 100 cm",
        "year": 2025,
        "edition": "Unique",
        "provenance": "Acquired directly from the artist through North Contemporary in Reykjavik.",
        "price": 420000,
        "starting_price": 280000,
        "listed_date": "March 2026",
        "sold": False,
        "image": "images/artworks/art_1.png",
    },
    {
        "id": 2,
        "title": "Whispering Pines",
        "artist": "Sigrún Eiríksdóttir",
        "seller": "Sigrún Eiríksdóttir",
        "seller_description": "Landscape watercolor artist inspired by Nordic nature and quiet wilderness scenes.",
        "medium": "Watercolor on paper",
        "style": "Contemporary Landscape",
        "dimensions": "70 × 50 cm",
        "year": 2023,
        "edition": "Unique",
        "provenance": "Originally exhibited at the Winter Light Exhibition in Akureyri before entering a private collection.",
        "price": 180000,
        "starting_price": 80000,
        "listed_date": "May 2026",
        "sold": True,
        "image": "images/artworks/art_2.png",
    },
    {
        "id": 3,
        "title": "Chromatic Reflection",
        "artist": "Lucien Vale",
        "seller": "Atelier V",
        "seller_description": "Contemporary art gallery.",
        "medium": "Acrylic on canvas",
        "style": "Abstract Expressionism",
        "dimensions": "120 × 120 cm",
        "year": 2025,
        "edition": "Unique",
        "provenance": "Featured in Atelier V's new Horizons collection before entering the current private collection.",
        "price": 520000,
        "starting_price": 300000,
        "listed_date": "April 2026",
        "sold": False,
        "image": "images/artworks/art_3.png",
    },
    {
        "id": 4,
        "title": "Still Bloom",
        "artist": "Camille Laurent",
        "seller": "Maison Alder",
        "seller_description": "Boutique contemporary gallery.",
        "medium": "Oil on linen",
        "style": "Contemporary Impressionism",
        "dimensions": "60 × 80 cm",
        "year": 2025,
        "edition": "...",
        "provenance": "A part of Maison Alder's Spring Collection featuring contemporary floral studies.",
        "price": 260000,
        "starting_price": 180000,
        "listed_date": "February 2026",
        "sold": False,
        "image": "images/artworks/art_4.png",
    },
    {
        "id": 5,
        "title": "Fragmented Silence",
        "artist": "Lucien Vale",
        "seller": "Atelier V",
        "seller_description": "Contemporary art gallery.",
        "medium": "Acrylic on canvas",
        "style": "Abstract Expressionism",
        "dimensions": "120 × 120 cm",
        "year": 2024,
        "edition": "Unique",
        "provenance": "Exhibeted as part of Lucien Vale's Color & Identity series at Atelier V.",
        "price": 600000,
        "starting_price": 200000,
        "listed_date": "April 2026",
        "sold": True,
        "image": "images/artworks/art_5.png",
    },
    {
        "id": 6,
        "title": "Tempest Tide",
        "artist": "Arnar Björnsson",
        "seller": "North Contemporary",
        "seller_description": "Contemporary gallery specializing in atmospheric Nordic-inspired and nature-focused works.",
        "medium": "Oil on canvas",
        "style": "Contemporary Seascape",
        "dimensions": "90 × 90 cm",
        "year": 2025,
        "edition": "Unique",
        "provenance": "Featured in North Contemporary's Northern Seas exhibition before entering a private collection.",
        "price": 340000,
        "starting_price": 300000,
        "listed_date": "May 2026",
        "sold": False,
        "image": "images/artworks/art_6.png",
    },
    {
        "id": 7,
        "title": "Sunlit Passage",
        "artist": "Isabella Moreau",
        "seller": "Isabella Moreau",
        "seller_description": "",
        "medium": "Acrylic on canvas",
        "style": "Contemporary Minimalism",
        "dimensions": "80 × 100 cm",
        "year": 2023,
        "edition": "Unique",
        "provenance": "A private collection.",
        "price": 100000,
        "starting_price": 120000,
        "listed_date": "April 2026",
        "sold": False,
        "image": "images/artworks/art_7.png",
    },
    {
        "id": 8,
        "title": "Quiet Presence",
        "artist": "Camille Laurent",
        "seller": "Maison Alder",
        "seller_description": "Boutique contemporary gallery.",
        "medium": "Oil on canvas",
        "style": "Contemporary Expressionism",
        "dimensions": "70 × 70 cm",
        "year": 2022,
        "edition": "Unique",
        "provenance": "Part of Camille Laurent's Reflections series presented at Maison Alder.",
        "price": 200000,
        "starting_price": 150000,
        "listed_date": "April 2026",
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