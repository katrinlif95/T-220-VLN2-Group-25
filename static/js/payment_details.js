// Get payment method dropdown element
const paymentMethod = document.getElementById("payment_method");

// Get payment method error message
const paymentMethodError = document.getElementById("payment-method-error");

// Get containers for each payment method section
const creditCardFields = document.getElementById("credit-card-fields");
const bankTransferFields = document.getElementById("bank-transfer-fields");
const wireTransferFields = document.getElementById("wire-transfer-fields");


// Show correct input fields depending
// on selected payment method
function updatePaymentFields() {

    // Hide all payment sections by default
    creditCardFields.style.display = "none";
    bankTransferFields.style.display = "none";
    wireTransferFields.style.display = "none";

    // Hide payment method error
    // once user selects a method
    if (paymentMethod.value && paymentMethodError) {
        paymentMethodError.style.display = "none";
    }

    // Show credit card fields
    if (paymentMethod.value === "credit_card") {
        creditCardFields.style.display = "grid";
    }

    // Show bank transfer fields
    if (paymentMethod.value === "bank_transfer") {
        bankTransferFields.style.display = "grid";
    }

    // Show wire transfer fields
    if (paymentMethod.value === "wire_transfer") {
        wireTransferFields.style.display = "grid";
    }
}

    // Update visible fields whenever
    // selected payment method changes
    paymentMethod.addEventListener("change", updatePaymentFields);


    // Run once when page loads
    // so correct fields are shown immediately
    updatePaymentFields();