from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .task import order_created

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
# import weasyprint
from django.utils.html import format_html

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid:
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])

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

# The staff_member_required decorator checks that both is_active and is_staff 
# fields of the user requesting the page are set to True.
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    pass
'''
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order':order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="order_{order.id}.pdf"'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])

    return response
'''
