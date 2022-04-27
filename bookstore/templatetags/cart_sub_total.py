from django import template
register = template.Library()
from bookstore.models import Cart,WebSettings

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
