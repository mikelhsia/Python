from django import forms
from django.utils.translation import gettext_lazy as _

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
	# This allows the user to select a quantity between 1-20. We use a TypedChoiceField field
	# with coerce=int to convert the input into an integer.
	quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label=_('Quantity'))

	# This allows you to indicate whether the quantity has to be added to any existing quantity in the cart
	# for this product (False), or if the existing quantity has to be updated with the given quantity (True).
	update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
