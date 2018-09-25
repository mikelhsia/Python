from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id):
	"""
	Task to send an e-mail notification when an order is successfully created
	:param order_id:
	:return:
	"""

	order = Order.objects.get(id=order_id)
	subject = f'Order no. {order.id}'
	message = f'Dear {order.first_name}, ' \
	          f'You have successfully placed an order' \
	          f'Your order id is {order.id}'

	# It's always recommended to pass only IDS to task functions and lookup objects when the task is executed.
	mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])

	return mail_sent