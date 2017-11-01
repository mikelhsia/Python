from django.contrib import admin
from blog.models import Article, Author, Tag

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'score', 'pub_date' ,'update_time')
 
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name','qq','addr','email')

admin.site.register(Tag)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Author, AuthorAdmin)
