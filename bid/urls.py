from django.urls import path

from . import views

urlpatterns = [
    path(
        "artworks/<int:artwork_id>/submit-bid/",
        views.submit_bid,
        name="submit-bid"
    ),
]