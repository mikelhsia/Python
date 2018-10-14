from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):

	def __init__(self, for_fields=None, *args, **kwargs):
		self.for_fields = for_fields
		super(OrderField, self).__init__(*args, **kwargs)

	def pre_save(self, model_instance, add):
		print(f'model_instance: {model_instance}')
		print(f'self.attname: {self.attname}')
		if getattr(model_instance, self.attname) is None:
			# No current value
			try:
				# Build a queryset to retrieve all objects for the field's model
				qs = self.model.objects.all()
				print(f'qs: {qs}')

				print(f'self.for_fields: {self.for_fields}')
				if self.for_fields:
					# filter by objects with the same field value for the fields in "for_fields"
					query = {field: getattr(model_instance, field) for field in self.for_fields}
					print(f'query: {query}')
					qs = qs.filter(**query)
					print(f'qs: {qs}')

				# get the order of the last item
				last_item = qs.latest(self.attname)
				value = last_item.order + 1
			except ObjectDoesNotExist:
				value = 0

			setattr(model_instance, self.attname, value)

			return value
		else:
			return super(OrderField, self).pre_save(model_instance, add)