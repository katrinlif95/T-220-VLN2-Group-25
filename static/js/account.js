// Profile image input field
const imageInput = document.getElementById(
    "id_profile_image"
);


// Profile image preview element
let imagePreview = document.getElementById(
    "profile-image-preview"
);


// Profile page success/error messages
const profileMessages = document.querySelector(
    ".profile-messages"
);


// Preview reminder message
const previewMessage = document.getElementById(
    "profile-preview-message"
);


// All profile form inputs
const formInputs = document.querySelectorAll(
    ".profile-form input"
);


// Hide existing success/error messages
function hideProfileMessages() {

    const existingMessages = document.querySelectorAll(
        ".profile-message:not(#profile-preview-message)"
    );

    existingMessages.forEach(message => {
        message.style.display = "none";
    });

}


// Show preview reminder message
function showPreviewMessage() {

    if (previewMessage) {

        previewMessage.style.display = "flex";

    }

}


// Add loading state to form submit buttons
function addSubmitLoadingState(formSelector, buttonSelector) {

    const form = document.querySelector(
        formSelector
    );

    const button = document.querySelector(
        buttonSelector
    );

    if (form && button) {

        form.addEventListener("submit", function() {

            button.disabled = true;
            button.textContent = "Updating...";

        });

    }

}


// Replace placeholder div with an image element
// when a new user selects a profile image
function ensureImagePreviewElement() {

    if (!imagePreview) {
        return null;
    }

    if (imagePreview.tagName.toLowerCase() === "img") {
        return imagePreview;
    }

    const newImagePreview = document.createElement("img");

    newImagePreview.id = "profile-image-preview";

    newImagePreview.className =
    "profile-image profile-image-placeholder clickable-profile-image";

    newImagePreview.alt = "Profile image preview";

    imagePreview.replaceWith(newImagePreview);

    imagePreview = newImagePreview;

    return imagePreview;

}


// Update preview image when user selects a new image
if (imageInput) {

    imageInput.addEventListener("change", function(event) {

        const file = event.target.files[0];

        if (file) {

            const previewElement = ensureImagePreviewElement();

            if (previewElement) {

                // Update profile image preview
                previewElement.src = URL.createObjectURL(file);

            }

            // Hide old success/error messages
            hideProfileMessages();

            // Show reminder to save changes
            showPreviewMessage();

        }

    });

}


// Hide success message and show preview reminder
// when user edits profile form fields
formInputs.forEach(input => {

    input.addEventListener("input", function() {

        hideProfileMessages();

        showPreviewMessage();

    });

});


// Profile update loading state
addSubmitLoadingState(
    ".profile-form",
    ".profile-update-btn"
);


// Contact information update loading state
addSubmitLoadingState(
    ".contact-form",
    "#update-contact-btn"
);