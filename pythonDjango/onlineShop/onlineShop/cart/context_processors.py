from .cart import Cart

# Create a context processor to set the current cart into the request context for template
def cart(request):
	# We instantiate the cart using the `request` object and make it available for the templates as a variable named `cart`
	return {'cart': Cart(request)}