from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum
from datetime import date
from django.utils.text import slugify



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)

    def __str__(self):
        return self.name    

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)
    barcode = models.CharField(max_length=100, null=True)
    minimum_stock = models.IntegerField(default=0)
    slug = models.SlugField(blank=True, null=True)


    #relationships
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def clean(self):
        if self.price <= 0:
            raise ValidationError("Price must be greater than 0")
        if self.quantity < 0:
            raise ValidationError("quantity cannot be negative")

    def reduce_stock(self, quantity):
        if self.quantity >= quantity:
            self.quantity -= quantity
            self.save()
            return True
        return False
    
    def replenish_stock(self, quantity):
        self.quantity += quantity
        self.save()

    def is_low_stock(self):
        return self.quantity <= self.minimum_stock    
   

class Customer(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
# previous sale model does not work as intended
# class Sale(models.Model):
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     date = models.DateTimeField(auto_now_add=True)
   
#     #relationships
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    

#     def __str__(self) -> str:
#         return f'Sale #{self.id} '
    
#     def clean(self):
#         if self.total_amount <= 0.00:
#             raise ValidationError("Total amount cannot be negative")
    
    # def get_total_amount(self):
    #     amount = self.items.all()
    #     self.total_amount += amount
    #     return self.total_amount
    
   
    
    # def save(self, *args, **kwargs):
    #     # self.total_amount = self.get_total_amount()
    #     self.clean()
    #     super().save(*args, **kwargs) 
        
        # for item in self.items.all():
        #     item.product.reduce_stock(item.quantity_sold)
      

    # def apply_discount(self, discount_percent):
    #     for item in self.items.all():
    #         item.apply_discount(discount_percent)

    # def apply_promotion(self, promotion):
    #     for item in self.items.all():
    #         item.apply_promotion(promotion)        

class SaleItem(models.Model):
    quantity_sold = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)

    #relationships
    
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    

    def __str__(self):
        return f'SaleItem {self.id} - {self.product.name}'
    
    def clean(self):
        if self.quantity_sold <= 0:
            raise ValidationError("Quantity sold must be greater than zero")
        if self.unit_price <= 0:
            raise ValidationError("Unit price must be greater than zero")
    def calculate_profit(self):
        product_cost = self.product.price
        profit = (self.unit_price - product_cost) * self.quantity_sold
        return profit  
    def apply_discount(self, discount_percent):
        original_subtotal = self.subtotal
        discount_amount = original_subtotal * (discount_percent / 100)
        self.subtotal = original_subtotal - discount_amount
        self.save()

    def apply_promotion(self, promotion):
        pass     
    
    def save(self, *args, **kwargs):
        self.subtotal = self.quantity_sold * self.unit_price
        self.profit = self.calculate_profit()
        self.clean()
        super().save(*args, **kwargs)
        self.product.reduce_stock(self.quantity_sold)
        
# created new sale model that works 
class Sale(models.Model):
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(auto_now_add=True)
   
    #relationships
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    saleitem = models.ForeignKey(SaleItem, on_delete=models.CASCADE, null=True, related_name='items')

    def __str__(self) -> str:
        return f'Sale #{self.id} '
    
    def clean(self):
        if self.total_amount <= 0.00:
            raise ValidationError("Total amount cannot be negative")
    
    def get_total_amount(self):
        amount = self.saleitem.subtotal
        self.total_amount += amount
        return self.total_amount
    
    def save(self, *args, **kwargs):
        self.total_amount = self.get_total_amount()
        self.clean()
        super().save(*args, **kwargs) 

    def apply_discount(self, discount_percent):
        discount = self.saleitem.apply_discount(discount_percent)
        return discount

    def apply_promotion(self, promotion):
        promo = self.saleitem.apply_promotion(promotion)
        return promo    
           
    
class Payment(models.Model):
    payment_method = models.CharField(max_length=100)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    change = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    #relationships
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'Payment for sale {self.sale.id}'
    
    def clean(self):
        if self.amount_paid < 0:
            raise ValidationError("Amount paid cannot be negative.")
        if self.change < 0:
            raise ValidationError("Change cannot be negative.")
    
class Employee(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    role = models.CharField(max_length=100)

    #relationships
    sales = models.ManyToManyField(Sale)  

    def __str__(self):
        return self.name  

class SalesReport(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    total_sales = models.IntegerField()
    total_profit = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"SalesReport {self.id}"  
    
    @classmethod
    def generate_report(cls, start_date, end_date):
        sales = Sale.objects.filter(date__range=(start_date, end_date))
        total_sales = sales.count()
        total_profit = sum(item.profit for sale in sales for item in sale.items.all())
        total_amount = sum(sale.total_amount for sale in sales)

        return cls.objects.create(
            start_date = start_date,
            end_date = end_date,
            total_sales = total_sales,
            total_profit = total_profit,
            total_amount = total_amount
            
        )
    def get_top_products(self, num_products=5):
        top_products = SaleItem.objects.filter(sale__date__range=(self.start_date, self.end_date)) \
            .values('product__name')\
            .annotate(total_quantity=Sum('quantity_sold')) \
            .order_by('-total_quantity') [:num_products]
        return top_products
    
    def get_total_sales_by_category(self):
         sales_by_category = SaleItem.objects.filter(sale__date__range=(self.start_date, self.end_date)) \
            .values('product__category__name') \
            .annotate(total_sales=Sum('subtotal')) \
            .order_by('-total_sales')
         return sales_by_category
    
    def get_total_sales_by_month(self):
        sales_by_month = Sale.objects.filter(date__range=(self.start_date, self.end_date)) \
            .extra({'month': "EXTRACT(month FROM date)"}) \
            .values('month') \
            .annotate(total_sales = Sum('total_amount')) \
            .order_by('month')
        return sales_by_month 
    
    def generate_low_stock_alert(self, threshold=10):
        low_stock_products = Product.objects.filter(quantity__lte=threshold)
        return low_stock_products
    
    def automate_stock_replenishment(self, threshold=10, replenishment_quantity=20):
        low_stock_products = self.generate_low_stock_alert(threshold)
        for product in low_stock_products:
            product.replenish_stock(replenishment_quantity)
        return len(low_stock_products)    








