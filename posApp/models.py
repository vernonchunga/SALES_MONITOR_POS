from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum
from datetime import datetime
from django.utils.text import slugify
from django.utils import timezone
from unicodedata import category



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100, null=True)
    status = models.IntegerField(default=1) 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.name 

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    order_price = models.FloatField(default=0)
    selling_price = models.FloatField(default=0)
    quantity = models.FloatField(default=1)
    code = models.CharField(max_length=100, null=True)
    minimum_stock = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)
    status = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 


    #relationships
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT)
    

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Products, self).save(*args, **kwargs)       
        
    
class Sales(models.Model):
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total  = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)


    
    def __str__(self) -> str:
        return f'Sale #{self.id}'
           

class SaleItems(models.Model):
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True, null=True)
    
    #relationships
    
    product_id = models.ForeignKey(Products, on_delete=models.PROTECT)
    sale_id = models.ForeignKey(Sales, on_delete=models.CASCADE, null=True, related_name='items')
    

    def __str__(self):
        return f'SaleItem {self.id} - {self.product_id.name}'
    
    
                
class SalesReport(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    No_of_sales = models.IntegerField(default=0)
    total_profit = models.FloatField(default=0)
    total_sales_ammount = models.FloatField(default=0)

   
    def generate_report(self):
        sales = Sales.objects.filter(date__range=(self.start_date, self.end_date))
        self.No_of_sales = sales.count()
        profit = SaleItems.objects.filter(date__range=(self.start_date, self.end_date)).aggregate(total = Sum('profit'))
        self.total_profit = profit['total'] or 0
        amount = Sales.objects.filter(date__range=(self.start_date, self.end_date)).aggregate(total = Sum('grand_total'))
        self.total_sales_ammount = amount['total'] or 0
        
        return self.total_sales_ammount
        
    def save(self, *args, **kwargs):
        self.No_of_sales = self.generate_report()
        self.total_profit = self.generate_report()
        self.total_sales_ammount  = self.generate_report()
        super().save(*args, **kwargs)
        
    # def get_top_products(self, num_products=5):
    #     top_products = SaleItem.objects.filter(sale__date__range=(self.start_date, self.end_date)) \
    #         .values('product__name')\
    #         .annotate(total_quantity=Sum('quantity_sold')) \
    #         .order_by('-total_quantity') [:num_products]
    #     return top_products
    
    # def get_total_sales_by_category(self):
    #      sales_by_category = SaleItem.objects.filter(sale__date__range=(self.start_date, self.end_date)) \
    #         .values('product__category__name') \
    #         .annotate(total_sales=Sum('subtotal')) \
    #         .order_by('-total_sales')
    #      return sales_by_category
    
    # def get_total_sales_by_month(self):
    #     sales_by_month = Sale.objects.filter(date__range=(self.start_date, self.end_date)) \
    #         .extra({'month': "EXTRACT(month FROM date)"}) \
    #         .values('month') \
    #         .annotate(total_sales = Sum('grand_total ')) \
    #         .order_by('month')
    #     return sales_by_month 
    
    # def generate_low_stock_alert(self, threshold=10):
    #     low_stock_products = Product.objects.filter(quantity__lte=threshold)
    #     return low_stock_products
    
    # def automate_stock_replenishment(self, threshold=10, replenishment_quantity=20):
    #     low_stock_products = self.generate_low_stock_alert(threshold)
    #     for product in low_stock_products:
    #         product.replenish_stock(replenishment_quantity)
    #     return len(low_stock_products)    








