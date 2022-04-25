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
    path('passwordreset/', passwordresetView, name="passwordreset" ),


     # user profile
    path('profile/', profile_view, name="profile" ),
   



    path('cart/', cart, name="cart" ),
    path('buy_now/', buy_now, name="buy_now" ),
    path('update_cart_item', update_cart_item, name="update_cart_item" ),
    path('checkout', checkout, name="checkout" ),

    # ajax
    path('api/get_book_by_category', get_all_books, name="get_books_by_cat" ),
    
    
    # location api
    path('get_districts', get_districts, name="get_districts" ),
    path('get_area', get_area, name="get_area" ),
]
