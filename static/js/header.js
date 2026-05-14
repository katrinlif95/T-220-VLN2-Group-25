/* USER DROPDOWN */

const dropdown = document.querySelector(".user-dropdown");
const trigger = document.querySelector(".user-trigger");

if (dropdown && trigger) {

    trigger.addEventListener("click", function (event) {

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