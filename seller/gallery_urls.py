from django.urls import path

from . import views

urlpatterns = [
    # http://127.0.0.1:8000/galleries/
    # Database version
    #path('', views.gallery_index, name='gallery-index'),

    # http://127.0.0.1:8000/galleries/{id}/ # kommenta þetta path þegar er ekki verið að nota dummy data
    # Database version
    #path('<int:seller_id>/', views.get_gallery_by_id, name='gallery-detail'),

    # fyrir dummy data
    path('<int:seller_id>/', views.gallery_detail_dummy, name='gallery-detail'),
    path('', views.gallery_index_dummy, name='gallery-index'),

]