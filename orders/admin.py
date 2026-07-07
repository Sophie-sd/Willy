from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display

from .models import Order, OrderItem


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'quantity', 'price', 'subtotal_display')
    can_delete = False

    @admin.display(description='Сума')
    def subtotal_display(self, obj):
        if obj.pk:
            return f'{obj.subtotal:.0f} ₴'
        return '—'

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        'number', 'customer_name', 'phone', 'total_display',
        'status_badge', 'created_at',
    )
    list_filter = ('status', 'delivery_method', 'created_at')
    search_fields = ('number', 'customer_name', 'phone', 'email')
    readonly_fields = (
        'number', 'total', 'created_at', 'updated_at',
    )
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Замовлення', {'fields': ('number', 'status', 'total', 'created_at', 'updated_at')}),
        ('Клієнт', {'fields': ('customer_name', 'phone', 'email', 'comment')}),
        ('Доставка', {'fields': ('delivery_method', 'delivery_city', 'delivery_address')}),
    )

    @display(description='Сума')
    def total_display(self, obj):
        return f'{obj.total:.0f} ₴'

    @display(
        description='Статус',
        label={
            'new': 'info',
            'paid': 'success',
            'shipped': 'warning',
            'done': 'success',
            'cancelled': 'danger',
        },
    )
    def status_badge(self, obj):
        return obj.status, obj.get_status_display()
