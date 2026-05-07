from django.urls import path

from . import views

urlpatterns = [
    # http://127.0.0.1:8000/artworks/
    path('', views.artwork_index, name='artwork-index'),
    path('<int:id>', views.get_artwork_by_id, name='artwork-by-id'),
# ath...
    path('<int:artwork_id>/', views.artwork_detail, name='artwork-detail'),
]

# hér þarf að samræma nafnavenjur, bæði fyrir id hvort það sé bara id eða artwork_id (seller_id osfrv)
# og hvort name sé artwork-detail eða artwork-by-id en artwork-detail og artwork_id er betra segir chat, meira lýsandi
# erum að nota artwork_detail og artist_detail og gallery_detail t.d. annarsstaðar