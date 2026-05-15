from django.urls import path
from . import  views

urlpatterns = [
    path('', views.home, name='home'),
    path("about/", views.about, name="about"),
    path("how-to-buy-art/",views.how_to_buy_art,name="how-to-buy-art"),
    path("how-to-sell-artwork/", views.how_to_sell_artwork, name="how-to-sell-artwork"),
    path("bidding-process/",views.bidding_process,name="bidding-process"),
    path("help-center/",views.help_center,name="help-center"),
    path("contact-support/",views.contact_support,name="contact-support"),
    path("report-an-issue/",views.report_an_issue,name="report-an-issue"),
    path("website-terms/",views.website_terms,name="website-terms"),
    path("privacy-policy/",views.privacy_policy,name="privacy-policy"),
]