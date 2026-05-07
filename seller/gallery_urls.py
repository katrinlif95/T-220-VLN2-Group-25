from django.urls import path

from . import views

urlpatterns = [
    # http://127.0.0.1:8000/galleries/
    path('', views.gallery_index, name='gallery-index'),

    # http://127.0.0.1:8000/galleries/{id}/
    path('<int:seller_id>/', views.get_gallery_by_id, name='gallery-detail'),
]