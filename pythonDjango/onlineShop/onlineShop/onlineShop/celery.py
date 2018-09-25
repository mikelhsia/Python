import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlineShop.settings')

app = Celery('onlineShop')

# We load any custom configuration from our project settings using the config_from_object() method.
app.config_from_object('django.conf:settings')

# Finally we tell Celery to auto-discover asynchronous tasks for the applications listed in
# the INSTALLED_APPS setting. Celery will look for a tasks.py file in each application directory
# to load asynchronous tasks defined in it.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)