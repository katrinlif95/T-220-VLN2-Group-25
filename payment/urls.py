from django.urls import path

from . import views

urlpatterns = [

    # Contact information page
    # http://127.0.0.1:8000/account/bids/3/finalize/contact/
    path(
        "<int:bid_id>/finalize/contact/",
        views.contact_information,
        name="finalize-contact"
    ),

    # Payment details page
    # http://127.0.0.1:8000/account/bids/3/finalize/payment/
    path(
        "<int:bid_id>/finalize/payment/",
        views.payment_details,
        name="finalize-payment"
    ),

    # Review page
    # http://127.0.0.1:8000/account/bids/3/finalize/review/
    path(
        "<int:bid_id>/finalize/review/",
        views.review_payment,
        name="finalize-review"
    ),

    # Confirm action, not really a page
    # http://127.0.0.1:8000/account/bids/3/finalize/confirm/
    path(
        "<int:bid_id>/finalize/confirm/",
        views.confirm_payment,
        name="finalize-confirm"
    ),

]