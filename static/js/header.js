/* USER DROPDOWN */

const dropdown = document.querySelector(".user-dropdown");
const arrow = document.querySelector(".dropdown-arrow-toggle");

if (dropdown && arrow) {

    arrow.addEventListener("click", function (event) {

        event.preventDefault();
        event.stopPropagation();

        dropdown.classList.toggle("open");
    });

    document.addEventListener("click", function () {
        dropdown.classList.remove("open");
    });

    dropdown.addEventListener("click", function (event) {
        event.stopPropagation();
    });
}