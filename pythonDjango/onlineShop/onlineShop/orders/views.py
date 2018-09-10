from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .task import order_created

# Create your views here.
def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid:
			order = form.save()
			for item in cart:
				OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
				                         quantity=item['quantity'])

			# Clear the cart
			cart.clear()

			# Launch asynchronous task
			order_created.delay(order.id) # Set the order in the session
                        request.session['order_id'] = order.id # redirect to the payment

                        return redirect(reverse('payment:process'))
			# return render(request, 'orders/order/created.html', {'order': order})

	else:
		form = OrderCreateForm()

	return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


