from django.contrib import admin
from .models import *

admin.site.register(Publishing_house)

@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'exists')
    list_display_links = ('name',)
    search_fields = ('name', 'price')
    list_editable = ('price', 'exists')
    list_filter = ('exists',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Passport_book)
class PassportAdmin(admin.ModelAdmin):
    pass

