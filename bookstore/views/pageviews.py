from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from bookstore.models import *
from django.template.loader import render_to_string
from django.contrib.auth.models import User

from django.conf import settings

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.


# import custom forms
from bookstore.forms import AddressForm

def book_store_home(request):
    single_category = None
    if 'cat_id' in request.GET:
        cat_id = request.GET.get('cat_id')
        try:
            single_category = Main_Category.objects.get(pk=cat_id)
        except:
            pass
    else:
        try:
            single_category = Main_Category.objects.first()
        except:
            pass

    context = {

        "single_category": single_category,
        "title": "Home-AAPLibrary"
    }
    return render(request, 'bookstore/home.html', context)


def get_all_books(request):
    if request.is_ajax():
        cat_id = request.POST.get('cat_id')
        single_category = Main_Category.objects.get(id=cat_id)
        if single_category:
            context = {
                "single_category": single_category,
            }
            html = render_to_string('bookstore/renderwithbooks.html', context)
            return JsonResponse({'html': html, 'success': True})
        else:
            return
    else:
        return HttpResponse("<h1>Not Found </h1>s")


def single_book(request, id, book_slug):
    if id and book_slug:
        try:
            book = Books.objects.get(pk=id)
            context = {
                "book": book,
            }

            return render(request, 'bookstore/single_book.html', context)
        except:
            return redirect('book_store_home')
    else:
        return HttpResponse("something wrong")





@login_required(login_url="login")
def cart(request):
    context = {}
    usercart = Cart.objects.filter(user=request.user.customers)
    context['usercart'] = usercart
    return render(request, 'bookstore/cart.html', context)
    pass


@login_required(login_url="login")
def buy_now(request):

    bookid = request.GET.get('id')
    try:
        book = Books.objects.get(pk=bookid)
    except:
        book=None
    if book is not None:
        try: 
            cart = Cart.objects.get(user=request.user.customers,book=book)
            cart.quantity +=1
            cart.save()
        except:
            
            cart = Cart(user=request.user.customers, book=book,quantity=1)
            cart.save()
    
    
    return redirect('cart')

def update_cart_item(request):
    if request.is_ajax():
        cart_item_id = request.GET.get('cartItemid')
        action = request.GET.get('action')
        try:
            cart = Cart.objects.get(pk=cart_item_id)

            if action == 'delete':
                cart.delete()
                usercart = Cart.objects.filter(user=request.user.customers)
                context = {'usercart':usercart}
                usercartList = render_to_string("bookstore/renderedcart.html",context)
                
                return JsonResponse({"status": "success","usercart" : usercartList})
                

            if action == 'increase': 
                cart.quantity +=1
            if action == 'decrease':
                if cart.quantity > 1:
                    cart.quantity -=1

            cart.save()
            return JsonResponse({"status":"success","quantity":cart.quantity})
        except:
            return JsonResponse({"status":"failed"})
    else:
        raise Exception("Error")
    
@login_required(login_url="login")

def checkout(request):
    addressForm = AddressForm()
    
    usercart = Cart.objects.filter(user=request.user.customers)

    context = {
        "usercart":usercart,
        "addressForm":addressForm,
    }

    return render(request, 'bookstore/checkout.html',context)