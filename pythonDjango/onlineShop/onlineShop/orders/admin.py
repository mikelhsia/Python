from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
# We use "ModelInline" for the OrderItem model to include it as an inline in the OrderAdmin class
class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created_at', 'updated_at']
	list_filter = ['paid', 'created_at', 'updated_at']
	# Inline allows you to include a model for appearing on the same edit page as the parent model
	inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
