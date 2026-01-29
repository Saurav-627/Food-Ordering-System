from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at', 'delivery_boy']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]
    actions = ['mark_as_accepted', 'mark_as_completed']

    def mark_as_accepted(self, request, queryset):
        queryset.update(status='ACCEPTED')
    mark_as_accepted.short_description = "Mark selected orders as Accepted"

    def mark_as_completed(self, request, queryset):
        queryset.update(status='COMPLETED')
    mark_as_completed.short_description = "Mark selected orders as Completed"

admin.site.register(Cart)
admin.site.register(CartItem)
