from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from .models import UserProfile, ContactInfo


class UserProfileAdmin(admin.ModelAdmin):
    # Fields shown in the admin list view
    list_display = (
        "user",
        "first_name",
        "last_name",
        "role",
        "profile_image_preview",
    )

    # Fields shown on the edit page
    fields = (
        "user",
        "role",
        "profile_image",
    )

    # Allows searching by username, first name and last name
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
    )

    # Adds a filter for user role
    list_filter = ("role",)

    # Show user's first name from Django User model
    def first_name(self, obj):
        return obj.user.first_name

    # Show user's last name from Django User model
    def last_name(self, obj):
        return obj.user.last_name

    # Shows a small clickable preview of uploaded profile image
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="height:50px; width:50px; object-fit:cover; border-radius:50%;" />'
                '</a>',
                obj.profile_image.url,
                obj.profile_image.url,
            )

        return "No image"

    # Column names in admin
    first_name.short_description = "First name"
    last_name.short_description = "Last name"
    profile_image_preview.short_description = "Profile image"


class ContactInfoAdmin(admin.ModelAdmin):
    # Fields shown in the admin list view
    list_display = ("user", "city", "country")

    # Allows searching by username and city
    search_fields = ("user__username", "city")

    # Adds a filter for country
    list_filter = ("country",)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ContactInfo, ContactInfoAdmin)