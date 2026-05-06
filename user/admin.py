from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from .models import UserProfile, ContactInfo


class UserProfileAdmin(admin.ModelAdmin):
    # Fields shown in the admin list view
    list_display = ("user", "role", "profile_image_preview")

    # Allows searching by username
    search_fields = ("user__username",)

    # Adds a filter for user role
    list_filter = ("role",)

    # Shows a small clickable preview of the profile image
    def profile_image_preview(self, obj):
        if obj.profile_image_url:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="height:50px; border-radius:50%;" />'
                '</a>',
                obj.profile_image_url,
                obj.profile_image_url
            )
        return "No image"

    # Column name in admin
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