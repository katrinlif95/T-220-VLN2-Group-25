from django.urls import path

from . import views

urlpatterns = [
    # http://127.0.0.1:8000/artwork
    path('', views.artwork_index, name='artwork-index'),
    path('<int:id>', views.get_artwork_by_id, name='artwork-by-id'),
]