from django import forms

class EmailCollectionForm(forms.Form):
	# This type of field is rendered as an <input type="text"> HTML element.
	name = forms.CharField(max_length=25)
	email = forms.EmailField()
	to = forms.EmailField()
	# In the comments field, we use a Textarea widget to display it as a <textarea> HTML element
	# instead of the default <input> element.
	comments = forms.CharField(required=True, widget=forms.Textarea)