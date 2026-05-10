from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from .models import Artwork, ArtworkImage


# Inline images inside Artwork admin (allows multiple images per artwork)
class ArtworkImageInline(admin.TabularInline):
    model = ArtworkImage
    extra = 1  # number of empty image fields shown

    fields = ("image_url", "alt_text", "order", "image_preview")
    readonly_fields = ("image_preview",)

    # Small preview of each image
    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="height:50px;" />',
                obj.image_url
            )
        return "No image"

    image_preview.short_description = "Preview"


# Custom admin configuration for Artwork model
class ArtworkAdmin(admin.ModelAdmin):

    # Updated list view (removed old single image preview)
    list_display = ("id", "title", "seller", "status", "listed_at", "display_order")

    # Add inline images here 👇
    inlines = [ArtworkImageInline]


# Optional: separate admin view for images (nice for debugging)
class ArtworkImageAdmin(admin.ModelAdmin):
    list_display = ("artwork", "order", "alt_text")


# Register models
admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(ArtworkImage, ArtworkImageAdmin)