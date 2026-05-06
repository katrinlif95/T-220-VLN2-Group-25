from django.contrib import admin

# Register your models here.
from .models import Bid


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):

    # Columns shown in admin list view
    list_display = (
        "user",
        "artwork",
        "amount",
        "status",
        "expires_at",
    )

    # Sidebar filters
    list_filter = (
        "status",
        "created_at",
    )

    # Search by username or artwork title
    search_fields = (
        "user__username",
        "artwork__title",
    )

    # Read-only fields in admin detail view
    readonly_fields = (
        "created_at",
        "updated_at",
        "cancelled_at",
    )

    # Default ordering (newest first)
    ordering = (
        "-created_at",
    )