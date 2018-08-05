from django import forms
from .models import PeekabooCollectionComment

# Remember that Django has two base classes to build forms: Form and ModelForm.

# Used the first one previously to let your users share posts by e-mail.
class EmailCollectionForm(forms.Form):
	# This type of field is rendered as an <input type="text"> HTML element.
	name = forms.CharField(max_length=25)
	email = forms.EmailField()
	to = forms.EmailField()
	# In the comments field, we use a Textarea widget to display it as a <textarea> HTML element
	# instead of the default <input> element.
	comments = forms.CharField(required=True, widget=forms.Textarea)


# In the this case, you will need to use ModelForm because you have to build a form dynamically from your Comment model.
class CommentForm(forms.ModelForm):
	class Meta:
		# Django introspects the model and builds the form dynamically for us
		model = PeekabooCollectionComment
		fields = ('name', 'email', 'body')