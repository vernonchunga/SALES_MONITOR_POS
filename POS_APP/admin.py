from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_info'] 

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'quantity', 'barcode', 'category']

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_info', 'address']

class SalesItemAdmin(admin.ModelAdmin):
    list_display = ['quantity_sold', 'unit_price', 'subtotal', 'product', 'profit']

class SalesAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_amount', 'customer', 'saleitem']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_method', 'amount_paid', 'change'] 

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', ] 

class SalesReportAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'total_sales', 'total_profit', 'total_amount'] 


admin.site.register(Category, CategoryAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(SaleItem, SalesItemAdmin)
admin.site.register(Sale, SalesAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(SalesReport, SalesReportAdmin)

