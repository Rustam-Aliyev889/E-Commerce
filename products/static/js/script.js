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
    // Obtain the CSRF token from the cookie
    const csrf_token = document.cookie.match(/csrftoken=([^ ;]+)/)[1];
    
    if (product_id !== 'undefined') {
        $.ajax({
            url: `/products/add-to-cart/${product_id}/`,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrf_token
            },
            data: {
                csrfmiddlewaretoken: csrf_token
            },
            dataType: 'json',
            success: function (data) {
                console.log('Item added to cart successfully:', data.product_name);
            },
            error: function (error) {
                console.error('Error adding item to cart:', error);
            }
        });
    }
}









console.log({ csrf_token })