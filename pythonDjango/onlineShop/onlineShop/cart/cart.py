from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon 

import inspect

def get_current_function_name():
    return inspect.stack()[1][3]

class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart
        :param request: Initialize a cart with request
        """
        # Save the session to make sure other function can access it
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        # print(f'{get_current_function_name()}: {cart}')

        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

        # Store current applied coupon
        self.coupon_id = self.session.get('coupon_id')


    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        :return:
        """
        product_ids = self.cart.keys()

        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']

            yield item


    def __len__(self):
        """
        Count all items in the cart
        :return:
        """
        return sum(item['quantity'] for item in self.cart.values())


    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
                

    def get_total_price(self):
        # print(f'{get_current_function_name()}: Price')
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


    def clear(self):
        """
        Remove cart from session
        :return:
        """
        # print(f'{get_current_function_name()}: {self.session[settings.CART_SESSION_ID]}')
        del self.session[settings.CART_SESSION_ID]

        self.session.modified = True

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity
        :param product:
        :param quantity:
        :param update_quantity:
        :return:
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price':str(product.price)}

        # print(f'{get_current_function_name()}: {self.cart[product_id]}')

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        """
        update the session cart
        :return:
        """
        self.session[settings.CART_SESSION_ID] = self.cart

        # Mark the session as 'modified' to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart
        :param product:
        :return:
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
