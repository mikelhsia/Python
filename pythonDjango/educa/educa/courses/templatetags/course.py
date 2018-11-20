from django import template

register = template.Library()

@register.filter
def model_name(obj):
	'''
	This is the model-name template filter. we can apply it in templates as object|model_name to get the
	model's name for an object
	:param obj:
	:return:
	'''
	try:
		return obj._meta.model_name
	except AttributeError:
		return None