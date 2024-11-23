from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from store.models import Collection, Customer, Order, OrderItem, Product
from django.db.models import Count
from django.utils.html import format_html, urlencode

# >>>> custom admin filters
class InventoryFilter(admin.SimpleListFilter):
    title  = 'inventory'
    parameter_name = 'inventory'
    def lookups(self, request, model_admin):
        return [('<10', 'Low')]
    
    def queryset(self, request, queryset: QuerySet[Any]):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

# >>>> admin view with custom columns and optimized sql query
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 12
    list_filter = ['collection', 'last_update', InventoryFilter ]
    list_select_related = ['collection']
    search_fields = ['title']

    @admin.display(ordering='collection__title')
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        return 'LOW' if product.inventory < 10 else 'OK'
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        inventory_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{inventory_count} products updates successfully'
        )


# >>>>> admin view with dynamic links
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_count' ]
    list_editable = ['membership']
    list_per_page = 12
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='order')
    def order_count(self, user):
        url = (
                reverse('admin:store_order_changelist')
                + '?'
                + urlencode({ "customer__id" :  user.id})
            )
        return format_html('<a href={}>{}</a>', url, user.order_count)
    

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(order_count=Count('order'))

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num=1
    max_num=10

# >>>>> admin view with inline classes
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'placed_at']
    list_per_page = 20
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']


# >>>> admin view with modified list
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    list_per_page = 20
    search_fields = ['title']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({'collection__id': str(collection.id)})
            )
        return format_html("<a href='{}' >{}</a>", url, collection.product_count)
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(product_count=Count('products'))
