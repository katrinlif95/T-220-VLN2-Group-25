from django.urls import path

from . import views

urlpatterns = [
    # http://127.0.0.1:8000/artists/
    path('', views.artist_index, name='artist-index'),

    # http://127.0.0.1:8000/artists/{id}/
    path('<int:seller_id>/', views.get_artist_by_id, name='artist-detail'),
]