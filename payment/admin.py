from django.contrib import admin

# Register your models here.
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    # Columns shown in admin list view
    list_display = (
        "user",
        "bid",
        "amount",
        "payment_method",
        "status",
        "created_at",
    )

    # Sidebar filters
    list_filter = (
        "payment_method",
        "status",
        "created_at",
    )

    # Search by username or artwork title
    search_fields = (
        "user__username",
        "bid__artwork__title",
    )

    # Read-only fields in admin detail view
    readonly_fields = (
        "created_at",
    )

    # Default ordering (newest first)
    ordering = (
        "-created_at",
    )