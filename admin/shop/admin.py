from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Flavor, Category, Application


class FlavorInline(admin.TabularInline):
    model = Flavor
    extra = 1
    fields = ['name', 'in_stock']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'strength', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'strength']
    list_editable = ['price', 'is_active']
    inlines = [FlavorInline]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'category', 'price', 'strength')
        }),
        ('Медиа', {
            'fields': ('photo',)
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category').prefetch_related('flavors')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'products_count', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']

    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Количество товаров'


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'customer_name', 'contact', 'status', 'total_amount', 'items_count']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'contact']
    readonly_fields = ['created_at', 'raw_payload', 'items_count']
    list_editable = ['status']
    
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('created_at', 'customer_name', 'contact', 'status', 'total_amount')
        }),
        ('Детали заказа', {
            'fields': ('raw_payload', 'items_count'),
            'classes': ('collapse',)
        }),
        ('Заметки', {
            'fields': ('notes',)
        }),
    )

    def items_count(self, obj):
        return obj.items_count
    items_count.short_description = 'Количество товаров'

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')


# Настройка админки
admin.site.site_header = "Pomoika Vape Lab - Админ панель"
admin.site.site_title = "Админ панель"
admin.site.index_title = "Управление магазином"
