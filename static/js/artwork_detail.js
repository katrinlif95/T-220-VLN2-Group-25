// Get artwork image data from Django json_script
const artworkImages = JSON.parse(
    document.getElementById("artwork-images").textContent
);


// Store index of currently displayed image
let currentImageIndex = 0;


// Update the main artwork image
function showImage(index) {

    // Get main image element
    const mainImage = document.getElementById(
        "main-artwork-image"
    );

    // Stop if image element or image data does not exist
    if (!mainImage || !artworkImages.length) {
        return;
    }

    // Update image source and alt text
    mainImage.src = artworkImages[index].url;
    mainImage.alt = artworkImages[index].alt;
}


// Show next image in carousel
function nextImage() {

    // Move to next image index
    currentImageIndex++;

    // Return to first image if end is reached
    if (currentImageIndex >= artworkImages.length) {
        currentImageIndex = 0;
    }

    // Update displayed image
    showImage(currentImageIndex);
}


// Show previous image in carousel
function previousImage() {

    // Move to previous image index
    currentImageIndex--;

    // Go to last image if beginning is passed
    if (currentImageIndex < 0) {
        currentImageIndex = artworkImages.length - 1;
    }

    // Update displayed image
    showImage(currentImageIndex);
}


// Make functions available to onclick in HTML
window.nextImage = nextImage;
window.previousImage = previousImage;