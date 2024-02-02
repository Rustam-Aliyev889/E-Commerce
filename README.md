# Radiant Rituals
## Description.
Welcome to Radiant Rituals, your ultimate destination for beauty in its purest form. More than an e-commerce platform, it's an experience crafted for beauty enthusiasts who appreciate excellence. Immerse yourself in a seamless journey through premium beauty products. Elevate your beauty routine with Radiant Rituals – your guide to timeless elegance.

## My motivation.
I built Radiant Rituals to challenge the norm in e-commerce design. Breaking away from the black-and-white mold, I wanted to show that web stores can reflect a company's energy and personality. With a vibrant and inviting design, Radiant Rituals proves that beauty and uniqueness can shine through in the digital world, offering a different and delightful shopping experience.

## Screenshots
###### The main page

![1 Main Page]<img src="/products/static/images/scr_shots/src_mp.jpeg">

    

## Tech Stack

The magic behind Radiant Rituals:

* **Frontend**: Crafted with love using HTML, CSS, and JavaScript to create a dynamic and delightful user interface.
* **Backend**: Powered by the elegance of Python and the efficiency of Django for a robust server-side experience.
* **Database**: SQLite3 stores the beauty secrets securely, ensuring efficient data management.
* **Framework**: Django, the heart of Radiant Rituals, orchestrates the seamless integration of frontend and backend components.
* **Styling**: Bootstrap adds a touch of modernity and responsiveness to the overall design.

## Features

| Feature  |  Coded?       | Description  |
|----------|:-------------:|:-------------|
| User Authentication | &#10004; | Users can register and log in securely to access personalized features.|
| Forgot Password | &#10004; | Reset your password through the "Forgot Password" functionality for enhanced account security and user convenience. |
| View Products | &#10004; | Explore our diverse catalog of beauty products with detailed information on each item. |
| Product Details | &#10004; | Product page with more details. |
|  Filters | &#10004; | filtering options to help users quickly find specific products based on categories |
| Shopping Cart Functionality | &#10004; | Add, remove, and view products in your shopping cart before proceeding to checkout. |
| Blog | &#10004; | Explore our blog for beauty tips, trends, and product recommendations to stay informed and inspired. |
| Stripe Payments | &#10004; | Experience seamless and secure payments through Stripe, supporting various payment methods for a hassle-free checkout process.|
|  Order Confirmation | &#10004; | Users receive a confirmation message summarizing their order details after successfully completing the checkout process. |
| Checkout | &#10004; | Safely and securely complete your purchase by providing shipping information, selecting a payment method, and confirming order details. |

## Installation

1. Clone the Repository

```sh
git clone https://github.com/Rustam-Aliyev889/E-Commerce.git
```

```sh
cd radiant_rituals
```

2. Apply migrations

```sh
python manage.py migrate
```

 3. Create Superuser (Optional)

```sh
python manage.py createsuperuser
```

4. Run the Development Server

```sh
python manage.py runserver
```
The development server will run at http://localhost:8000/. Visit this URL in your web browser to access the application.

## Usage
1. Explore the Website
Visit the website at http://localhost:8000/ to explore the beauty products, read the blog, and enjoy the overall experience.

2. Admin Panel
Access the Django admin panel at http://localhost:8000/admin/ using the superuser credentials created earlier. Here, you can manage products, user accounts, and more.

