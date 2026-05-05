from django.http import HttpResponse

def artist_index(request):
    return HttpResponse(f"All artists: {request.path}")

def get_artist_by_id(request, id):
    return HttpResponse(f"Artist page: {request.path} with id {id}")
def gallery_index(request):
    return HttpResponse(f"All galleries: {request.path}")
def get_gallery_by_id(request, id):
    return HttpResponse(f"Gallery page: {request.path} with id {id}")