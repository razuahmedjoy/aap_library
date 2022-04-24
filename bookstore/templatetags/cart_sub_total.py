from django import template
register = template.Library()
from bookstore.models import Cart

@register.simple_tag
def cart_sub_total(usercart):
    subtotal = 0
    for item in usercart:
        subtotal += item.total_amount
    return subtotal

@register.simple_tag
def total_cart_item(user):
   
    cart = Cart.objects.filter(user__contact_no=user.username)
    return len(cart)
