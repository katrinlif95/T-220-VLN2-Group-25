from django.urls import path

from . import views

urlpatterns = [

    # Contact information page
    path(
        "<int:bid_id>/contact/",
        views.contact_information,
        name="finalize-contact"
    ),

    # Payment details page
    path(
        "<int:bid_id>/payment/",
        views.payment_details,
        name="finalize-payment"
    ),

    # Review page
    path(
        "<int:bid_id>/review/",
        views.review_payment,
        name="finalize-review"
    ),

    # Confirm action
    path(
        "<int:bid_id>/confirm/",
        views.confirm_payment,
        name="finalize-confirm"
    ),
]