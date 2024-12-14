from django.contrib import admin
from django.utils.html import format_html
from .models import Contact, Product, Orders, OrderUpdate

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'created_at')
    search_fields = ('name', 'email', 'phone_number')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'subcategory', 'price', 'display_image')
    search_fields = ('product_name', 'category', 'subcategory')
    list_filter = ('category', 'subcategory')
    list_editable = ('price',)

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.image.url
            )
        return 'No Image'
    display_image.short_description = 'Product Image'

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'order_id', 'user', 'name', 'email', 'amount', 
        'payment_status', 'get_order_date'
    )
    search_fields = ('name', 'email', 'order_id')
    list_filter = ('payment_status',) 
    readonly_fields = ('order_id', 'payment_token')

    def get_order_date(self, obj):
        try:
            return obj.oid.split('-')[1] if '-' in obj.oid else 'N/A'
        except:
            return 'N/A'
    get_order_date.short_description = 'Order Date'

@admin.register(OrderUpdate)
class OrderUpdateAdmin(admin.ModelAdmin):
    list_display = ('update_id', 'order_id', 'update_desc', 'delivered', 'timestamp')
    list_filter = ('delivered', 'timestamp')
    search_fields = ('order_id', 'update_desc')
    list_editable = ('delivered',)

admin.site.site_header = 'Apple Tech E-Commerce Admin'
admin.site.site_title = 'Apple Tech Admin Portal'
admin.site.index_title = 'Welcome to Apple Tech Administration'