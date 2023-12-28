document.addEventListener('DOMContentLoaded', function () {
    //to get the current URL
    var currentUrl = window.location.href;

    // Finds all buttons with the 'filter-button' class
    var buttons = document.querySelectorAll('.filter-button');

    // Loop through the buttons
    buttons.forEach(function (button) {
        // Checks if the button's URL matches the current URL
        if (button.href === currentUrl) {
            // If it matches, adds the 'active' class to highlight the button
            button.classList.add('active');
        }
    });
});
