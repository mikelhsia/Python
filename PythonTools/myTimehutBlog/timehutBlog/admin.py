from django.contrib import admin
from .models import Collection, Moment

class CollectionAdmin(admin.ModelAdmin):
	list_display = ('collection_id', 'baby_id', 'slug', 'content_type', 
		'caption', 'updated_at', 'created_at')
	list_filter = ('content_type', 'updated_at', 'baby_id')
	search_fields = ('caption',)

	# When edit collection_id field, this will prepopulate the slug field with the 
	# input of the title field using the prepopulated_fields attribute
	prepopulated_fields = {'slug': ('collection_id',)}

	ordering = ['created_at', 'collection_id']

class MomentAdmin(admin.ModelAdmin):
	list_display = ('moment_id', 'event_id', 'baby_id' , 'slug', 'content_type', 
		'src_url', 'content', 'updated_at', 'created_at')
	list_filter = ('content_type', 'updated_at', 'baby_id')
	search_fields = ('content',)
	prepopulated_fields = {'slug': ('moment_id',)}

	# Need to be a foreign key, this enable a better user-friendly foreign key search popup
	raw_id_fields = ('event_id',)
	
	ordering = ['created_at', 'moment_id']

# Register your models here.
# admin.site.register(Collection)
admin.site.register(Collection, CollectionAdmin)
# admin.site.register(Moment)
admin.site.register(Moment, MomentAdmin)

