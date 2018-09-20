from django.contrib import admin
from .models import Order, OrderItem

import csv
import datetime
from django.http import HttpResponse

# Register your models here.
# We use "ModelInline" for the OrderItem model to include it as an inline in the OrderAdmin class
class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ['product']

def export_to_csv(modeladmin, request, queryset):
	opts = modeladmin.model._meta
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = f'attachment; filename={opts.verbose_name}.csv'
	writer = csv.writer(response)

	fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
	# Write a first row with header information
	writer.writerow([field.verbose_name for field in fields])
	# Write data
	for obj in queryset:
		data_row = []
		for field in fields:
			value = getattr(obj, field.name)
			if isinstance(value, datetime.datetime):
				value = value.strftime('%d/%m/%Y')
			data_row.append(value)
		writer.writerow(data_row)

	return response
export_to_csv.short_description = 'Export to CSV'

def get_all_field(modeladmin, request, queryset):
	opts = modeladmin.model._meta
	print(f'Fields: {opts.get_fields()}')
	print(f'Column: {queryset[0]}')

get_all_field.short_description = 'Print fields on Console'

class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created_at', 'updated_at']
	list_filter = ['paid', 'created_at', 'updated_at']
	# Inline allows you to include a model for appearing on the same edit page as the parent model
	inlines = [OrderItemInline]

	# Add export to csv action
	actions = [export_to_csv, get_all_field]

admin.site.register(Order, OrderAdmin)
