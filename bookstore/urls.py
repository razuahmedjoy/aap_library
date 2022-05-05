from django.contrib import admin
from django.urls import path, include



# views
from .views import *
from .locations import *
urlpatterns = [
    path('', book_store_home, name="book_store_home" ),
    path('book/<int:id>/<str:book_slug>/', single_book, name="single_book" ),

    # authentication
    path('register/', register, name="register" ),
    path('createaccount/', createaccount, name="createaccount" ),
    path('login/', login_view, name="login" ),
    path('logout/', LogoutView, name="logout" ),
    path('search_books/', search_books, name="search_books" ),
    path('passwordreset/', passwordresetView, name="passwordreset" ),


     # user profile
    path('profile/', profile_view, name="profile" ),
   



    path('cart/', cart, name="cart" ),
    path('buy_now/', buy_now, name="buy_now" ),
    path('update_cart_item', update_cart_item, name="update_cart_item" ),
    path('checkout', checkout, name="checkout" ),
    path("addressbook/", default_address, name="addressbook"),


    #add to cart
    path('add_to_cart', add_to_cart, name="add_to_cart" ),

    # user review
    path('write_review/<int:id>', write_review, name="write_review"),

    # ask a question
    path('write_question/<int:id>', write_question, name="write_question"),


    # ajax
    path('api/get_book_by_category', get_all_books, name="get_books_by_cat" ),
    
    
    # location api
    path('get_districts', get_districts, name="get_districts" ),
    path('get_area', get_area, name="get_area" ),
]
