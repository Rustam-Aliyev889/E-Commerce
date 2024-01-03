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

// custom.js

function addToCart(product_id) {
    $.ajax({
        url: '/products/add-to-cart/19/',
        type: 'POST',
        data: {'csrfmiddlewaretoken': '{{ csrf_token }}'},
        success: function (data) {
            console.log('Item added to cart successfully:', data.message);
            // Perform any additional client-side actions here.
        },
        error: function (error) {
            console.error('Error adding item to cart:', error);
        }
    });
}



console.log('hello')