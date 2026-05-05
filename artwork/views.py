from django.http import HttpResponse
from django.shortcuts import render

def artwork_index(request):
    return render(request, "artwork/artworks.html")

def get_artwork_by_id(request, id):
    return HttpResponse(f"Artwork page: {request.path} with id {id}")