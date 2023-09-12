from django.contrib import admin
from . import models
from django.db.models.aggregates import Count
from django.utils.html import format_html
from django.urls import reverse 
from django.utils.http import urlencode

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>=10', 'OK'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        if self.value() == '>=10':
            return queryset.filter(inventory__gte=10)
        
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    exclude = ['promotions']
    prepopulated_fields = {
        'slug': ['title']
    }
    autocomplete_fields = ['collection']
    list_display = ['title', 'unit_price', 'inventory', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 25
    list_filter = ['last_update', 'collection', InventoryFilter]
    search_fields = ['title'] 
    list_select_related = ['collection']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    def collection_title(self, product):
        return product.collection.title
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products were successfully updated', level='success')

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 25
    list_filter = ['membership']
    search_fields = ['first_name', 'first_name__istartswith', 'last_name__istartswith']

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    min_num = 1
    max_num = 10
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer_full_name']
    list_per_page = 25
    search_fields = ['customer_full_name'] 
    list_select_related = ['customer']

    def customer_full_name(self, order):
        return order.customer.first_name + " " + order.customer.last_name


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    list_per_page = 25
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({'collection__id': str(collection.id)})
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )
