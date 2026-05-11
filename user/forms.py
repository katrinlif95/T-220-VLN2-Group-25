from django import forms


class ProfileUpdateForm(forms.Form):
    first_name = forms.CharField(
        label="First name",
        max_length=150,
        required=True,
    )

    last_name = forms.CharField(
        label="Last name",
        max_length=150,
        required=True,
    )

    profile_image = forms.ImageField(
        label="Profile image",
        required=False,
    )