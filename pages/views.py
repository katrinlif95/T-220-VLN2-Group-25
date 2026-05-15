from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html")

def about(request):
    return render(request, "pages/about.html")

def how_to_buy_art(request):
    return render(request, "pages/user_guide/how_to_buy_art.html")

def how_to_sell_artwork(request):
    return render(request, "pages/user_guide/how_to_sell_artwork.html")

def bidding_process(request):
    return render(request, "pages/user_guide/bidding_process.html")

def help_center(request):
    return render(request, "pages/support/help_center.html")

def contact_support(request):
    return render(request, "pages/support/contact_support.html")

def report_an_issue(request):
    return render(request, "pages/support/report_an_issue.html")

def website_terms(request):
    return render(request, "pages/website_terms.html")

def privacy_policy(request):
    return render(request, "pages/privacy_policy.html")