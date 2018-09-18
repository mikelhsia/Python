from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': f'{order.get_total_cost().quantize(Decimal(".01")):.2f}',
        'item_name': f'Order {order.id}',
        'invoice': f'str(order.id)',
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("payment:done")}',
        'cancel_return': f'http://{host}{reverse("payment:canceled")}',
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'order': order, 'form': form})


# We use the csrf_exempt decorator to avoid Django expecting a CSRF token, since PayPal can redirect the user to any of these views via POST. 
@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
