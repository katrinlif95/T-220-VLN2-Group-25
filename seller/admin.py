from django.contrib import admin
from .models import Seller


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "display_name",
        "seller_type",
        "user",
        "city",
    )

    list_filter = (
        "seller_type",
    )

    search_fields = (
        "display_name",
        "user__username",
    )

    ordering = (
        "id",
    )