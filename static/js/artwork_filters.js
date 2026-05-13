/* FILTER ELEMENTS */

const filterForm = document.querySelector(".artwork-filters");

const priceToggle = document.getElementById("price-filter-toggle");
const priceMenu = document.getElementById("price-filter-menu");

const searchWrapper = document.querySelector(".filter-search");
const searchToggle = document.getElementById("search-toggle");
const searchToggleIcon = document.getElementById("search-toggle-icon");
const searchInput = document.getElementById("artwork-search-input");

const minPriceSlider = document.getElementById("min-price");
const maxPriceSlider = document.getElementById("max-price");

const minPriceValue = document.getElementById("min-price-value");
const maxPriceValue = document.getElementById("max-price-value");

const dualRangeTrack = document.getElementById("dual-range-track");


/* FORMAT ISK */

function formatISK(value) {
    return Number(value)
        .toString()
        .replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}


/* SUBMIT FILTERS */

function submitArtworkFilters(clearField = null) {

    if (!filterForm) {
        return;
    }

    const params = new URLSearchParams();
    const fields = filterForm.querySelectorAll("input, select");

    fields.forEach((field) => {

        if (
            clearField === "price"
            && (
                field.name === "min_price"
                || field.name === "max_price"
            )
        ) {
            return;
        }

        if (field.name === clearField) {
            return;
        }

        if (!field.value) {
            return;
        }

        if (
            field.name === "min_price"
            && field.value === field.min
        ) {
            return;
        }

        if (
            field.name === "max_price"
            && field.value === field.max
        ) {
            return;
        }

        params.append(field.name, field.value);
    });

    const queryString = params.toString();

    if (queryString) {
        window.location.href =
            `${window.location.pathname}?${queryString}`;
    } else {
        window.location.href = window.location.pathname;
    }
}


/* PRICE DROPDOWN */

if (priceToggle && priceMenu) {
    priceToggle.addEventListener("click", () => {
        priceMenu.classList.toggle("hidden");
    });
}


/* EXPANDING SEARCH */

if (searchToggle && searchWrapper && searchInput && searchToggleIcon) {

    const activeSearch = (
        searchWrapper.dataset.activeSearch || ""
    ).trim();

    function getCurrentSearch() {
        return searchInput.value;
    }

    function updateSearchIcon() {
        const currentSearch = getCurrentSearch();

        if (
            activeSearch !== ""
            && currentSearch === activeSearch
        ) {
            searchToggleIcon.textContent = "close";
        } else {
            searchToggleIcon.textContent = "search";
        }
    }

    updateSearchIcon();

    searchToggle.addEventListener("click", () => {
        const isOpen = searchWrapper.classList.contains(
            "search-open"
        );

        const currentSearch = getCurrentSearch();

        // Closed -> open search
        if (!isOpen) {
            searchWrapper.classList.add("search-open");
            searchInput.focus();
            return;
        }

        // Open + unchanged active search -> clear search
        if (
            activeSearch !== ""
            && currentSearch === activeSearch
        ) {
            searchInput.value = "";
            submitArtworkFilters("search");
            return;
        }

        // Open + empty -> close search
        if (currentSearch === "") {
            searchWrapper.classList.remove("search-open");
            return;
        }

        // Open + new/changed search -> submit search
        submitArtworkFilters();
    });

    searchInput.addEventListener("input", () => {
        updateSearchIcon();
    });

    searchInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            submitArtworkFilters();
        }
    });
}


/* PRICE RANGE SLIDERS */

function updatePriceValues() {

    if (!minPriceSlider || !maxPriceSlider) {
        return;
    }

    let minValue = Number(minPriceSlider.value);
    let maxValue = Number(maxPriceSlider.value);

    if (minValue > maxValue) {
        minValue = maxValue;
        minPriceSlider.value = minValue;
    }

    if (minPriceValue) {
        minPriceValue.textContent = formatISK(minValue);
    }

    if (maxPriceValue) {
        maxPriceValue.textContent = formatISK(maxValue);
    }

    const min = Number(minPriceSlider.min);
    const max = Number(maxPriceSlider.max);

    const leftPercent = ((minValue - min) / (max - min)) * 100;
    const rightPercent = ((maxValue - min) / (max - min)) * 100;

    if (dualRangeTrack) {
        dualRangeTrack.style.left = `${leftPercent}%`;
        dualRangeTrack.style.width = `${rightPercent - leftPercent}%`;
    }
}

if (minPriceSlider && maxPriceSlider) {
    updatePriceValues();

    minPriceSlider.addEventListener("input", updatePriceValues);
    maxPriceSlider.addEventListener("input", updatePriceValues);

    minPriceSlider.addEventListener("change", () => {
        submitArtworkFilters();
    });

    maxPriceSlider.addEventListener("change", () => {
        submitArtworkFilters();
    });
}


/* AUTO-SUBMIT SELECT FILTERS */

document.querySelectorAll(".auto-submit-filter").forEach((filter) => {
    filter.addEventListener("change", () => {
        submitArtworkFilters();
    });
});


/* CLEAR SINGLE FILTER */

document.querySelectorAll(".filter-clear-button").forEach((button) => {

    button.addEventListener("click", (event) => {

        // Prevent dropdown toggle
        event.stopPropagation();

        submitArtworkFilters(button.dataset.clearFilter);
    });
});