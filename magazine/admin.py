from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'FIO_agent', 'agent_telephone')
    list_display_links = ('name',)
    search_fields = ('name','FIO_agent',)
    list_editable = ('agent_telephone',)
    list_filter = ('is_exists',)
    ordering = ('name',)

    @admin.display(description='ФИО Представителя')
    def FIO_agent(self, obj):
        if obj.agent_patronymic:
            return f"{obj.agent_firstname} {obj.agent_name[0]}. {obj.agent_patronymic[0]}."
        return f"{obj.agent_firstname} {obj.agent_name[0]}."

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    pass
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
@admin.register(Pos_supply)
class Pos_supplyAdmin(admin.ModelAdmin):
    pass
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
@admin.register(Pos_order)
class Pos_orderAdmin(admin.ModelAdmin):
    pass
@admin.register(Parametr)
class ParametrAdmin(admin.ModelAdmin):
    pass
@admin.register(Pos_parametr)
class Pos_parametrAdmin(admin.ModelAdmin):
    pass
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass