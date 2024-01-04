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
                const messageContainer = document.getElementById('cartMessageContainer');
                messageContainer.innerHTML = `"${data.product_name}" added to cart successfully.`;

                messageContainer.style.display = 'block';
                messageContainer.style.position = 'fixed';
                messageContainer.style.textAlign = 'center';
                messageContainer.style.top = '0'
                messageContainer.style.left = '50%';
                messageContainer.style.transform = 'translateX(-50%)';
                messageContainer.style.backgroundColor = '#4CAF50';
                messageContainer.style.color = 'white';
                messageContainer.style.padding = '15px';
                messageContainer.style.zIndex = '1000';

                setTimeout(() => {
                    messageContainer.innerHTML = '';
                    messageContainer.style.display = 'none';
                }, 3500);
                /*console.log('Item added to cart successfully:', data.product_name);*/
            },
            error: function (error) {
                const messageContainer = document.getElementById('cartMessageContainer');
                messageContainer.innerHTML = 'Error adding item to cart: ' + error;

                messageContainer.style.display = 'block';
                messageContainer.style.position = 'fixed';
                messageContainer.style.textAlign = 'center';
                messageContainer.style.top = '0'
                messageContainer.style.left = '50%';
                messageContainer.style.transform = 'translateX(-50%)';
                messageContainer.style.backgroundColor = '#8B0000';
                messageContainer.style.color = 'white';
                messageContainer.style.padding = '15px';
                messageContainer.style.zIndex = '1000';

                setTimeout(() => {
                    messageContainer.innerHTML = '';
                    messageContainer.style.display = 'none';
                }, 3500);
                /*console.error('Error adding item to cart:', error);*/
            }
        });
    }
}









console.log({ csrf_token })