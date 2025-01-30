from django.contrib import admin
from .models import (
    Operation, 
    OperationCustomer, 
    OperationSalesPrice, 
    OperationDay, 
    OperationItem, 
    OperationSubItem
)

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ['reference_number', 'buyer_company', 'start_date', 'end_date', 'status', 'total_pax', 'is_active']
    list_filter = ['status', 'is_active', 'company', 'branch']
    search_fields = ['reference_number', 'buyer_company__name']
    date_hierarchy = 'start_date'

@admin.register(OperationCustomer)
class OperationCustomerAdmin(admin.ModelAdmin):
    list_display = ['operation', 'first_name', 'last_name', 'customer_type', 'is_buyer', 'is_active']
    list_filter = ['customer_type', 'is_buyer', 'is_active']
    search_fields = ['first_name', 'last_name', 'passport_no']

@admin.register(OperationSalesPrice)
class OperationSalesPriceAdmin(admin.ModelAdmin):
    list_display = ['operation', 'price', 'currency', 'is_active']
    list_filter = ['currency', 'is_active']

@admin.register(OperationDay)
class OperationDayAdmin(admin.ModelAdmin):
    list_display = ['operation', 'date', 'is_active']
    list_filter = ['is_active']
    date_hierarchy = 'date'

@admin.register(OperationItem)
class OperationItemAdmin(admin.ModelAdmin):
    list_display = ['operation_day', 'item_type', 'pick_time', 'is_active']
    list_filter = ['item_type', 'is_active']
    search_fields = ['notes']

@admin.register(OperationSubItem)
class OperationSubItemAdmin(admin.ModelAdmin):
    list_display = ['operation_item', 'subitem_type', 'ordering', 'is_active']
    list_filter = ['subitem_type', 'is_active']
    ordering = ['operation_item', 'ordering']
