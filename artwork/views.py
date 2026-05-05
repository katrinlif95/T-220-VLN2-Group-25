from django.http import HttpResponse

def artwork_index(request):
    return HttpResponse(f"All artworks: {request.path}")

def get_artwork_by_id(request, id):
    return HttpResponse(f"Artwork page: {request.path} with id {id}")