from xml.dom import ValidationErr
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from bookstore.models import *
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from time import time
from django.conf import settings

from django.urls import reverse



from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string

# Create your views here.


# import custom forms
from bookstore.forms import *


def book_store_home(request):
    single_category = None
    all_category = None
    if "cat_id" in request.GET:
        cat_id = request.GET.get("cat_id")
        try:
            single_category = Main_Category.objects.get(pk=cat_id)
        except:
            pass
    else:
        try:
            all_category = Main_Category.objects.all()
        except:
            pass

    context = {
        "single_category": single_category,
        "all_category": all_category,
        "title": "Home-AAPLibrary",
    }
    return render(request, "bookstore/home.html", context)


def get_all_books(request):
    if request.is_ajax():
        cat_id = request.POST.get("cat_id")
        single_category = Main_Category.objects.get(id=cat_id)
        if single_category:
            context = {
                "single_category": single_category,
            }
            html = render_to_string("bookstore/renderwithbooks.html", context)
            return JsonResponse({"html": html, "success": True})
        else:
            return
    else:
        return HttpResponse("<h1>Not Found </h1>s")


def single_book(request, id, book_slug):
    if request.user.is_authenticated:
        current_customer = Customers.objects.get(user=request.user)
        orders = Order.objects.filter(customer=current_customer)

        if id and book_slug:
            try:
                book = Books.objects.get(pk=id)
            except:
                return redirect("book_store_home")

            review_form = ReviewForm()
            # review_form = None
            qna_form = QnAForm()

            context = {
                "book": book,
                "review_form": review_form,
                "orders": orders,
                "qa_form": qna_form,
            }

            return render(request, "bookstore/single_book.html", context)

    else:
        if id and book_slug:
            try:
                book = Books.objects.get(pk=id)
                context = {
                    "book": book,
                }
                return render(request, "bookstore/single_book.html", context)
            except:
                return redirect("book_store_home")

    return HttpResponse("something wrong")


@login_required(login_url="login")
def write_review(request, id):
    if request.method == "POST":
        book = Books.objects.get(id=id)
        user = Customers.objects.get(user=request.user)
        comment = request.POST.get("comment")
        rating = request.POST.get("ratings")
        review = Review(book=book, user=user, comment=comment, ratings=rating)

        try:
            review.full_clean()
            review.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        except ValidationError:
            pass


@login_required(login_url="login")
def write_question(request, id):
    if request.method == "POST":
        book = Books.objects.get(id=id)
        user = Customers.objects.get(user=request.user)
        q = request.POST.get("question")
        question = QnA(book=book, user=user, question=q)

        try:
            question.full_clean()
            question.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        except ValidationError:
            pass


@login_required(login_url="login")
def cart(request):
    context = {}
    usercart = Cart.objects.filter(user=request.user.customers)
    context["usercart"] = usercart
    return render(request, "bookstore/cart.html", context)
    pass


@login_required(login_url="login")
def buy_now(request):

    bookid = request.GET.get("id")
    try:
        book = Books.objects.get(pk=bookid)
    except:
        book = None
    if book is not None:
        try:
            cart = Cart.objects.get(user=request.user.customers, book=book)
            cart.quantity += 1
            cart.save()
        except:

            cart = Cart(user=request.user.customers, book=book, quantity=1)
            cart.save()

    return redirect("cart")


# add to cart view
@login_required(login_url="login")
def add_to_cart(request):
    if request.is_ajax():
        bookid = request.GET.get("bookid")
        action = request.GET.get("action")

        try:
            book = Books.objects.get(pk=bookid)
        except:
            book = None

        if action == "add_to_cart":
            if book is not None:
                try:
                    cart = Cart.objects.get(user=request.user.customers, book=book)
                    user_cart = Cart.objects.filter(
                        user__contact_no=request.user.username
                    )
                    return JsonResponse(
                        {"status": "exists", "message": "Book already added to cart"}
                    )
                except:
                    cart = Cart(user=request.user.customers, book=book, quantity=1)
                    cart.save()
                    user_cart = Cart.objects.filter(
                        user__contact_no=request.user.username
                    )
                    return JsonResponse({"status": "success", "count": len(user_cart)})

    else:
        raise Exception("Error")


def update_cart_item(request):
    if request.is_ajax():
        cart_item_id = request.GET.get("cartItemid")
        action = request.GET.get("action")
        try:
            cart = Cart.objects.get(pk=cart_item_id)

            if action == "delete":
                cart.delete()
                usercart = Cart.objects.filter(user=request.user.customers)
                context = {"usercart": usercart}
                usercartList = render_to_string("bookstore/renderedcart.html", context)

                return JsonResponse({"status": "success", "usercart": usercartList})

            if action == "increase":
                cart.quantity += 1
            if action == "decrease":
                if cart.quantity > 1:
                    cart.quantity -= 1

            cart.save()
            return JsonResponse({"status": "success", "quantity": cart.quantity})
        except:
            return JsonResponse({"status": "failed"})
    else:
        raise Exception("Error")


@login_required(login_url="login")
def profile_view(request):

    current_customer = Customers.objects.get(user=request.user)
    orders = Order.objects.filter(customer=current_customer)

    context = {"orders": orders, "customer": current_customer}

    return render(request, "bookstore/profile.html", context)


@login_required(login_url="login")
def checkout(request):
    current_user = request.user
    addressForm = AddressForm(instance=current_user)
    paymentForm = PaymentForm(instance=current_user)

    usercart = Cart.objects.filter(user=request.user.customers)
    try:
        web_settings = WebSettings.objects.last()
    except:
        web_settings = None
        

    if request.method == "POST":

        district = request.POST["district"]
        area = request.POST["area"]
        address = request.POST["address"]
        contact_no = request.POST["contact_no"]
        payment_method = request.POST["payment_method"]
        sender_number = request.POST["sender_number"]
        transaction_id = request.POST["transaction_id"]

        total_amount = int(request.POST["total_amount"])

        customer = Customers.objects.get(user=request.user)

        # create payment
        newPayment = Payment(
            customer=customer,
            sender_number=sender_number,
            payment_method=payment_method,
            transaction_id=transaction_id,
            total_amount=total_amount,
        )

        # generate orderid
        order_id = f"AAP-{get_random_string(8).upper()}{int(time())}"
        newPayment.order_id = order_id
        newPayment.save()

        # set address
        newOrderAddress = Address(
            user=customer,
            district=district,
            area=area,
            address=address,
            contact_no=contact_no,
        )
        newOrderAddress.save()

        # create order
        newOrder = Order(
            customer=customer,
            contact_no=contact_no,
            grand_total=total_amount,
            address=newOrderAddress,
            order_id=order_id,
            payment=newPayment,
        )
        newOrder.save()

        for item in usercart:
            orderd_product = OrderedProducts()
            orderd_product.order = newOrder
            orderd_product.customer = customer
            orderd_product.books = item.book
            orderd_product.quantity = item.quantity
            orderd_product.price = item.price
            orderd_product.total_amount = item.total_amount
            orderd_product.save()

        Cart.objects.filter(user=customer).delete()
        order = newOrder

        context = {
            "order_id": order_id,
            "order": order,
        }
        return render(request, "bookstore/ordercomplete.html", context)

    if len(usercart) == 0:
        return HttpResponse(
            "You dont have any product on your cart. Please Add some product"
        )

    context = {
        "usercart": usercart,
        "addressForm": addressForm,
        "paymentForm": paymentForm,
        "web_settings": web_settings,
    }

    return render(request, "bookstore/checkout.html", context)



@login_required(login_url="login")
def default_address(request):
    current_user = request.user
    addressForm = AddressForm(instance=current_user)
    customer = request.user.customers

    if request.is_ajax():
        action = request.GET.get("action")
        if action == "updateaddress":
            address = SavedAddress.objects.get(user=current_user.customers)
            return JsonResponse({"status": "success", "district": address.district, 
            "area": address.area, "address": address.address, "contact": address.contact_no})

   

    if request.method == "GET":
        return render(
            request,
            "bookstore/addressbook",
            {
                "addressForm": addressForm,
            },
        )

    if request.method == "POST":

        try:
            address = SavedAddress.objects.get(user=current_user.customers)
            address.district = request.POST["district"]
            address.area = request.POST["area"]
            address.address = request.POST["address"]
            address.contact_no = request.POST["contact_no"]
            address.save()
            return render(
            request,
            "bookstore/addressbook",
            {
                "addressForm": addressForm,
                "message" : "Address Edited Succesfully!"
            },
        )

        
        except:
            district = request.POST["district"]
            area = request.POST["area"]
            address = request.POST["address"]
            contact_no = request.POST["contact_no"]
            saved_a = SavedAddress(user=customer, district=district, area=area,address=address, contact_no=contact_no)
            saved_a.save()

            return render(
            request,
            "bookstore/addressbook",
            {
                "addressForm": addressForm,
                "message" : "New Address Added Succesfully!"
            },
        )


            



        
        
            
        
        

   
        
           
