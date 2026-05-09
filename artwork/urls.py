from django.urls import path

from . import views

urlpatterns = [

    # http://127.0.0.1:8000/artworks/
    path('', views.artwork_index, name='artwork-index'),

    # http://127.0.0.1:8000/artworks/{artwork_id}/
    path('<int:artwork_id>/', views.artwork_detail, name='artwork-detail'),
]