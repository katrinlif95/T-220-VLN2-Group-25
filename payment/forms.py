from django import forms

from .models import Payment

# Import Python regular expressions
# for payment format validation
import re

class ContactInfoForm(forms.Form):

    street_address = forms.CharField(
        required=True,
        error_messages={
            "required": "Street address is required."
        }
    )

    city = forms.CharField(
        required=True,
        error_messages={
            "required": "City is required."
        }
    )

    postal_code = forms.CharField(
        required=True,
        error_messages={
            "required": "Postal code is required."
        }
    )

    country = forms.CharField(
        required=True,
        error_messages={
            "required": "Country is required."
        }
    )

    national_id = forms.CharField(
        required=True,
        error_messages={
            "required": "National ID is required."
        }
    )

    def clean_national_id(self):

        national_id = self.cleaned_data["national_id"]

        if not national_id.isdigit():
            raise forms.ValidationError(
                "National ID must contain digits only."
            )

        return national_id


class PaymentDetailsForm(forms.Form):

    payment_method = forms.ChoiceField(
        choices=Payment.PAYMENT_METHOD_CHOICES,
        required=True,
        error_messages={
            "required": "Payment method is required."
        }
    )

    card_name = forms.CharField(required=False)
    card_number = forms.CharField(required=False)
    expiry_date = forms.CharField(required=False)
    cvc = forms.CharField(required=False)

    bank_account = forms.CharField(required=False)

    sending_bank = forms.CharField(required=False)
    routing_number = forms.CharField(required=False)
    account_number = forms.CharField(required=False)

    def clean(self):

        cleaned_data = super().clean()

        payment_method = cleaned_data.get("payment_method")

        if payment_method == Payment.METHOD_CREDIT_CARD:

            # Get submitted card name
            card_name = cleaned_data.get("card_name", "")

            # Validate card name is filled out
            if not card_name:
                self.add_error(
                    "card_name",
                    "Name on card is required."
                )

            # Validate card name contains letters only
            elif not all(
                    char.isalpha() or char.isspace()
                    for char in card_name
            ):
                self.add_error(
                    "card_name",
                    "Name on card must contain letters only."
                )

            # Validate credit card number format
            # Example: 0000 0000 0000 0000
            card_number = cleaned_data.get("card_number", "")

            # Remove spaces before validation
            card_number_digits = card_number.replace(" ", "")

            if not card_number:
                self.add_error(
                    "card_number",
                    "Card number is required."
                )

            elif (
                not card_number_digits.isdigit()
                or len(card_number_digits) != 16
            ):
                self.add_error(
                    "card_number",
                    "Card number must be in format 0000 0000 0000 0000."
                )

            # Validate expiry date format
            # Example: MM/YY
            expiry_date = cleaned_data.get("expiry_date", "")

            expiry_date_pattern = r"^(0[1-9]|1[0-2])\/\d{2}$"

            if not expiry_date:
                self.add_error(
                    "expiry_date",
                    "Expiry date is required."
                )

            elif not re.match(expiry_date_pattern, expiry_date):
                self.add_error(
                    "expiry_date",
                    "Expiry date must be in MM/YY format."
                )

            # Validate CVC format
            # Example: 000
            cvc = cleaned_data.get("cvc", "")

            if not cvc:
                self.add_error(
                    "cvc",
                    "CVC is required."
                )

            elif not cvc.isdigit() or len(cvc) != 3:
                self.add_error(
                    "cvc",
                    "CVC must be 3 digits."
                )

        elif payment_method == Payment.METHOD_BANK_TRANSFER:

            # Validate bank account format
            # Example: 0000-00-000000
            bank_account = cleaned_data.get("bank_account", "")

            bank_account_pattern = r"^\d{4}-\d{2}-\d{6}$"

            if not bank_account:
                self.add_error(
                    "bank_account",
                    "Bank account is required."
                )

            elif not re.match(bank_account_pattern, bank_account):
                self.add_error(
                    "bank_account",
                    "Bank account must be in format 0000-00-000000."
                )

        elif payment_method == Payment.METHOD_WIRE_TRANSFER:

            if not cleaned_data.get("sending_bank"):
                self.add_error(
                    "sending_bank",
                    "Sending bank is required."
                )

            routing_number = cleaned_data.get("routing_number", "")

            if not routing_number:
                self.add_error(
                    "routing_number",
                    "Routing number is required."
                )

            elif not routing_number.isdigit():
                self.add_error(
                    "routing_number",
                    "Routing number must contain digits only."
                )

            account_number = cleaned_data.get("account_number", "")

            if not account_number:
                self.add_error(
                    "account_number",
                    "Account number is required."
                )

            elif not account_number.isdigit():
                self.add_error(
                    "account_number",
                    "Account number must contain digits only."
                )

        return cleaned_data