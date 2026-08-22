from decimal import Decimal
from catalog.models import Product
from constants import AppConstants

_constants = AppConstants.get_instance()


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(_constants.CART_SESSION_KEY)
        if not cart:
            cart = self.session[_constants.CART_SESSION_KEY] = {}
        self.cart = cart

    def _validate_quantity(self, quantity):
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

    def add(self, product, quantity=1, override_quantity=False):
        self._validate_quantity(quantity)
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def update_quantity(self, product, quantity):
        self._validate_quantity(quantity)
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clean_deleted_products(self):
        db_ids = set(str(pid) for pid in Product.objects.filter(id__in=list(self.cart.keys())).values_list('id', flat=True))
        deleted_ids = [pid for pid in list(self.cart.keys()) if pid not in db_ids]
        for pid in deleted_ids:
            del self.cart[pid]
        if deleted_ids:
            self.save()

    def clear(self):
        self.cart.clear()
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        products = Product.objects.filter(id__in=self.cart.keys())
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            if 'product' in item:
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
