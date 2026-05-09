from django.urls import path

from . import views

urlpatterns = [
    # http://127.0.0.1:8000/artists/
    # Database versions
    # path('', views.artist_index, name='artist-index'),

    # http://127.0.0.1:8000/artists/{id}/
    # path('<int:seller_id>/', views.get_artist_by_id, name='artist-detail'),


    # Dummy versions
    path('', views.artist_index_dummy, name='artist-index'), # kommenta þetta út og afkommenta fyrir ofan fyrir gagnagrunn

    path('<int:seller_id>/', views.artist_detail_dummy, name='artist-detail'),
]
