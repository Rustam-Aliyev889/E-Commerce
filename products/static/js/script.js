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

const BASE_URL = '/products/'; 

function updateCartCount() {
    const cartItemCount = document.getElementById('cartItemCount');

    if (cartItemCount) {
        $.ajax({
            url: BASE_URL + 'get-cart-count/', 
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                console.log('Server response:', data);

                if (data.item_count > 0) {
                    console.log('Updating cart count:', data.item_count);
                    cartItemCount.innerHTML = data.item_count;
                    cartItemCount.style.display = 'inline-block';  // Shows the badge
                } else {
                    console.log('Hiding cart count.');
                    cartItemCount.style.display = 'none';  //  the badge if count is 0
                }
            },
            error: function (error) {
                console.error('Error updating cart count:', error);
            }
        });
    } else {
        console.error('Element with ID "cartItemCount" not found.');
    }
}


$(document).ready(function () {
    updateCartCount();
});


function addToCart(product_id) {
    let quantity = 1;  // Default quantity
    const inputQuantity = document.getElementById('inputQuantity');
    if (inputQuantity) {
        quantity = parseInt(inputQuantity.value, 10);
        }
    console.log('Quantity:', quantity);
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
                csrfmiddlewaretoken: csrf_token,
                quantity: quantity
            },
            dataType: 'json',
            success: function (data) {
                const messageContainer = document.getElementById('cartMessageContainer');
                messageContainer.innerHTML = `"${data.product_name}"  added to cart successfully.`;

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
                }, 3000);
                updateCartCount();
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