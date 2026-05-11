// Get submit bid modal elements
const openBidModalButton = document.getElementById("open-bid-modal");
const closeBidModalButton = document.getElementById("close-bid-modal");
const bidModal = document.getElementById("bid-modal");

// Get submit bid form + input fields
const bidForm = document.getElementById("submit-bid-form");

const amountInput = document.getElementById("bid-amount");
const expirationInput = document.getElementById("bid-expiration");

// Get validation error message containers
const amountError = document.getElementById("amount-error");
const expirationError = document.getElementById("expiration-error");
const bidFormError = document.getElementById("bid-form-error");


// Only run modal functionality if all required elements exist
if (openBidModalButton && closeBidModalButton && bidModal) {

    // Open bid modal when user clicks submit/resubmit button
    openBidModalButton.addEventListener("click", function () {
        bidModal.classList.remove("hidden");
    });


    // Close bid modal when user clicks close button
    closeBidModalButton.addEventListener("click", function () {

        // Hide modal
        bidModal.classList.add("hidden");

        // Clear form inputs
        if (bidForm) {
            bidForm.reset();
        }

        // Clear validation errors
        if (amountError) {
            amountError.textContent = "";
        }

        if (expirationError) {
            expirationError.textContent = "";
        }

        if (bidFormError) {
            bidFormError.textContent = "";
        }

    });

}


// Validate bid form before submission
if (
    bidForm
    && amountInput
    && expirationInput
    && amountError
    && expirationError
    && bidFormError
) {

    bidForm.addEventListener("submit", function (event) {

        // Assume form is valid initially
        let isValid = true;

        // Clear previous validation errors
        amountError.textContent = "";
        expirationError.textContent = "";
        bidFormError.textContent = "";

        // Get entered bid amount
        const amount = Number(amountInput.value);

        // Get minimum valid bid amount
        // This is highest bid if one exists,
        // otherwise the artwork starting price
        const minBid = parseFloat(
            bidForm.dataset.minBid
        );

        // Get selected expiration date
        const expirationDate = new Date(
            expirationInput.value
        );

        // Get today's date without time
        const today = new Date();
        today.setHours(0, 0, 0, 0);


        // Validate that amount is a positive number
        if (!amount || amount <= 0) {

            amountError.textContent =
                "Please enter a valid bid amount.";

            isValid = false;
        }

        // Validate that amount is not below minimum bid
        else if (amount < minBid) {

            amountError.textContent =
                "Please enter a higher bid amount.";

            isValid = false;
        }


        // Validate expiration date
        if (
            !expirationInput.value
            || expirationDate <= today
        ) {

            expirationError.textContent =
                "Expiration date must be in the future.";

            isValid = false;
        }


        // Get existing pending bid data, if user is resubmitting
        const existingAmount = Number(
            bidForm.dataset.existingAmount
        );

        const existingExpiration =
            bidForm.dataset.existingExpiration;


        // Validate that resubmitted bid contains
        // at least one actual change
        if (
            isValid
            && existingAmount
            && existingExpiration
            && amount === existingAmount
            && expirationInput.value === existingExpiration
        ) {

            bidFormError.textContent =
                "No changes made, nothing to resubmit.";

            isValid = false;
        }


        // Prevent form submission if validation fails
        if (!isValid) {
            event.preventDefault();
        }

    });

}