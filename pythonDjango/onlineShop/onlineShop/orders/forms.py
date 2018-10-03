from django import forms
from .models import Order

# from localflavor.us.forms import USZipCodeField

class OrderCreateForm(forms.ModelForm):
    # We import the USZipCodeField field from the us package of localflavor
    # and use it for the postal_code field of the OrderCreateForm form
    # postal_code = USZipCodeField()
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
