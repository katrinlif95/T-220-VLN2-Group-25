from django.shortcuts import render

# Create your views here.
# Main account/profile page
# Displays general user profile information
def profile_detail(request):

    return render(
        request,
        "user/profile_detail.html"
    )


# Page showing all bids belonging to the logged-in user
def account_bids(request):

    return render(
        request,
        "user/account_bids.html"
    )


# Page for viewing and editing user contact information
def contact_information(request):

    return render(
        request,
        "user/contact_information.html"
    )