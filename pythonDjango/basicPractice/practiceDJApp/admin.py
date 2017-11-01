from django.contrib import admin
from practiceDJApp.models import Test, Contact, Tag

# Register your models here.
class TagInline(admin.TabularInline):
	model = Tag


class ContactAdmin(admin.ModelAdmin):
	# 以上代码定义了一个 ContactAdmin 类，用以说明管理页面的显示格式。
	# 里面的 fields 属性定义了要显示的字段。
	# fields = ('name', 'email')

	# 在列表中显示更多的栏目，只需要在 ContactAdmin 中增加 list_display 属性
	list_display = ('name', 'age', 'email')  # list

	search_fields = ('name',)

	# Contact 是 Tag 的外部键，所以有外部参考的关系。
	# 而在默认的页面显示中，将两者分离开来，无法体现出两者的从属关系。
	# 我们可以使用内联显示，让 Tag 附加在 Contact 的编辑页面上显示。
	inlines = [TagInline]  # Inline

	fieldsets = (
		['Main', {
			'fields': ('name', 'email'),
		}],
		['Advance', {
			'classes': ('collapse',),  # CSS
			'fields': ('age',),
		}]
	)


admin.site.register(Contact, ContactAdmin)
# admin.site.register([Test, Tag])
admin.site.register(Test)
