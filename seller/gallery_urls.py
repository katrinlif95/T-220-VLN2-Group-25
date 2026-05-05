from django.urls import path

from . import views

urlpatterns = [
    # http://127.0.0.1:8000/gallery
    path('', views.gallery_index, name='gallery-index'),

    # http://127.0.0.1:8000/gallery/{id}
    path('<int:id>', views.get_gallery_by_id, name='gallery-by-id'),
]