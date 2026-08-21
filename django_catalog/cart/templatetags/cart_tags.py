from django import template

register = template.Library()


@register.filter
def get_cart_quantity(cart, product):
    if not cart or not hasattr(cart, 'cart'):
        return 0
    item = cart.cart.get(str(product.id))
    return item['quantity'] if item else 0
