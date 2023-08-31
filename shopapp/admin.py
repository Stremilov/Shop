from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Models, Order

from .admin_mixins import ExportAsCSVMixins


class OrderInline(admin.TabularInline):
    model = Models.orders.through


class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.action(description='Archive products')
def make_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchive products')
def make_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Models)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixins):
    actions = [
        'export_csv',
        make_archived,
        make_unarchived,
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    search_fields = 'description', 'name'
    fieldsets = [
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Price options', {
            'fields': ('price', 'discount'),
            'classes': ('collapse',),
        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': 'Extra option to archieve.',
        }),
    ]

    def description_short(self, obj: Models) -> str:
        if len(obj.description) < 50:
            return obj.description
        return obj.description[:50] + '...'




@admin.register(Order)
class Orderadmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = 'delivery_adress', "promocode", 'created_time', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('user')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username
