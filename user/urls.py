from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

# URL routes for user account related pages
urlpatterns = [

    path('register/', views.register, name='register'),

    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),

    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # Main account/profile page
    # Example: /account/
    path(
        '',
        views.profile_detail,
        name='account-profile'
    ),

    # Page showing all bids belonging to the logged-in user
    # Example: /account/bids/
    path(
        'bids/',
        views.account_bids,
        name='account-bids'
    ),

    # Page for viewing/editing user contact information
    # Example: /account/contact-information/
    path(
        'contact-information/',
        views.contact_information,
        name='account-contact'
    ),
]