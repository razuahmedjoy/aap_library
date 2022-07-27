from django import template
register = template.Library()
from bookstore.models import Cart, Notification,WebSettings

@register.simple_tag
def get_shipping_charge():
    try:
        settings = WebSettings.objects.last()
        shipping_charge = settings.shipping_charge
    except:
        shipping_charge = 0
    return shipping_charge



@register.simple_tag
def cart_sub_total(usercart):
    subtotal = 0
    shipping_charge = get_shipping_charge()

    for item in usercart:
        subtotal += item.total_amount
    return subtotal + shipping_charge

@register.simple_tag
def total_cart_item(user):
    cart = Cart.objects.filter(user__contact_no=user.username)
    return len(cart)


@register.simple_tag
def unread_notification(user):
    cart = Notification.objects.filter(user__contact_no=user.username, read=False)
    return len(cart)


@register.simple_tag
def cart_sub_total_free(usercart):
    subtotal = 0
    shipping_charge = get_shipping_charge()

    for item in usercart:
        subtotal += item.total_amount
    return subtotal


@register.simple_tag
def deduct_delivery(current_method):
    shipping_charge = get_shipping_charge()
    final_price = current_method - shipping_charge
    return final_price


@register.simple_tag
def ordered_books(order):
        book_list = []
        for book in order.ordered_books.all():
            if book.quantity > 1:
                b = f"{book}({book.quantity})"
                book_list.append(b)
            else:
                b = f"{book}"
                book_list.append(b)
                 
        return book_list