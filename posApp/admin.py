from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'order_price', 'selling_price', 'quantity', 'code', 'category_id']

class SalesAdmin(admin.ModelAdmin):
    list_display = ['code', 'sub_total', 'grand_total']

class SalesItemAdmin(admin.ModelAdmin):
    list_display = ['qty', 'price', 'total', 'profit', 'product_id']

class SalesReportAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'No_of_sales', 'total_profit', 'total_sales_ammount'] 


admin.site.register(Category, CategoryAdmin)
admin.site.register(Products, ProductAdmin)
admin.site.register(Sales, SalesAdmin)
admin.site.register(SaleItems, SalesItemAdmin)
admin.site.register(SalesReport, SalesReportAdmin)

