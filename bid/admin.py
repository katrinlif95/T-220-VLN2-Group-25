from django.contrib import admin

# Register your models here.
from .models import Bid


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):

    # Columns shown in admin list view
    list_display = (
        "id",
        "user",
        "artwork",
        "amount",
        "expires_at",
        "status",
        "payment_status",
    )

    # Sidebar filters
    list_filter = (
        "artwork",
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
        "id",
        "payment_status",
        "created_at",
        "updated_at",
        "cancelled_at",
    )

    # Default ordering (newest first)
    ordering = (
        "-created_at",
    )

    def payment_status(self, obj):
        payment = obj.payments.first()

        if payment:
            return payment.get_status_display()

        return "No payment"