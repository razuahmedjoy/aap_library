from django import template
register = template.Library()

@register.simple_tag
def cart_sub_total(usercart):
    subtotal = 0
    for item in usercart:
        subtotal += item.total_amount
    return subtotal