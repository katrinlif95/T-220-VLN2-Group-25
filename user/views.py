from django.shortcuts import render

# Create your views here.
from bid.models import Bid
from django.contrib.auth.models import User  #má taka út þegar login flow er orðið virkt og hardcoded test búið

# Main account/profile page
# Displays general user profile information
def profile_detail(request):

    return render(
        request,
        "user/profile_detail.html"
    )


# Page showing all bids belonging to the logged-in user
def account_bids(request):
    # FINAL VERSION : Get all bids belonging to current logged-in user
    # bids = Bid.objects.filter(
        #user=request.user
    #)


    # TEMPORARY TEST VERSION: (svo það þurfi ekki að vera logged in til að sjá bids)
    # Manually fetch a specific test user from database
    test_user = User.objects.get(
        username="User1"
    )

    # Get bids belonging to test user
    bids = Bid.objects.filter(
        user=test_user
    )

    return render(
        request,
        "user/account_bids.html",
        {
            "bids": bids
        }
    )


# Page for viewing and editing user contact information
def contact_information(request):

    return render(
        request,
        "user/contact_information.html"
    )