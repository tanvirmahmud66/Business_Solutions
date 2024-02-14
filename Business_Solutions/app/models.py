from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import os

# Create your models here.

# ------------------------------------------------ Device Categories Model
class Categories(models.Model):
    category = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.category
    


# ------------------------------------------------ Brand Model 
class Brand(models.Model):
    brand = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.brand
    

#------------------------------------------------- supplier model
class Supplier(models.Model):
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.company_name


# ------------------------------------------------ Devices Model
def product_image_path(instance, filename):
    return os.path.join('Product_Image', f'{instance.model}', filename)

class Product(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    price = models.PositiveBigIntegerField()
    cost = models.PositiveBigIntegerField()
    description = models.TextField()
    productImg = models.ImageField(upload_to=product_image_path, null=True, blank=True)
    released_year = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.model
    


# -------------------------------------------------- Inventory Model
class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, unique=True)
    quantity = models.PositiveIntegerField()
    supplierId = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.product.model



class Transaction(models.Model):
    TRANSACTION_TYPE = [
        ('IN', 'IN'),
        ('OUT','OUT')
    ]
    PAYMENT_METHOD = [
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit card'),
        ('Master Card', 'Master Card'),
        ('Bank Cheque','Bank cheque'),
        ('Bkash','Bkash'),
        ('Sure Cash','Sure Cash'),
        ('DBBL Mobile','DBBL Mobile'),
        ('DBBL Card','DBBL Card'),
        ('Nagad','Nagad'),
        ('UCash', 'UCash'),
        ('Payoneer','Payoneer'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=5,choices=TRANSACTION_TYPE)
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD)
    quantity = models.PositiveIntegerField()
    amount = models.PositiveBigIntegerField()
    transaction_code = models.CharField(max_length=255,unique=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['transaction_date']


    def __str__(self):
        return self.transaction_code