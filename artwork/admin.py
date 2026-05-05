from django.contrib import admin

# Register your models here.
from .models import Artwork
from django.utils.html import format_html


# Custom admin configuration for Artwork model
class ArtworkAdmin(admin.ModelAdmin):

    # Fields displayed in the admin list view
    list_display = ("title", "image_preview")

    # Method to render an image preview from image_url
    def image_preview(self, obj):
        # Check if the artwork has an image URL
        if obj.image_url:
            # Return HTML for a clickable thumbnail image
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="height:50px;" />'
                '</a>',
                obj.image_url,  # link to full image
                obj.image_url   # image source
            )
        # Fallback text if no image is provided
        return "No image"

    # Set column header name in admin
    image_preview.short_description = "Image"


# Register the model with the custom admin class
admin.site.register(Artwork, ArtworkAdmin)