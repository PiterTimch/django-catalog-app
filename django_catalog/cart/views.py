from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from catalog.models import Product
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (ValueError, TypeError):
        quantity = 1

    override = request.POST.get("override", "False").lower() in ("true", "1")
    if quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=override)

    return redirect("cart:cart_detail")


@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity > 0:
        cart.update_quantity(product=product, quantity=quantity)
    else:
        cart.remove(product=product)

    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect("cart:cart_detail")


@require_POST
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    cart.clean_deleted_products()
    return render(request, "cart/detail.html", {"cart": cart})
