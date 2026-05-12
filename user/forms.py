import re
from django import forms
from django.contrib.auth.models import User


class ProfileUpdateForm(forms.Form):

    first_name = forms.CharField(
        label="First name",
        max_length=50,
        required=True,
    )

    last_name = forms.CharField(
        label="Last name",
        max_length=50,
        required=True,
    )

    profile_image = forms.ImageField(
        label="Profile image",
        required=False,
    )

    def clean_first_name(self):
        first_name = self.cleaned_data.get(
            "first_name"
        )

        return self.validate_name(
            first_name,
            "First name"
        )

    def clean_last_name(self):
        last_name = self.cleaned_data.get(
            "last_name"
        )

        return self.validate_name(
            last_name,
            "Last name"
        )

    def validate_name(self, value, field_name):

        # Remove leading/trailing whitespace
        value = value.strip()

        # Prevent extremely long names
        if len(value) > 25:
            raise forms.ValidationError(
                f"• {field_name} cannot be longer than 25 characters."
            )

        # Allow only letters, spaces,
        # hyphens and apostrophes
        if not re.match(
            r"^[A-Za-zÁÉÍÓÚÝÞÆÖáéíóúýþæöÐð\s'-]+$",
            value
        ):
            raise forms.ValidationError(
                f"• {field_name} can only contain letters, spaces, hyphens and apostrophes."
            )

        return value