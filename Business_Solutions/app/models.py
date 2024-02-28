from django.db import models
from multiupload.fields import MultiFileField
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




# ------------------------------------------------ Devices Model
def product_image_path(instance, filename):
    return os.path.join('Product_Image', f'{instance.model}', filename)


class Product(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    cost = models.PositiveIntegerField(null=True,blank=True)
    price = models.PositiveIntegerField(null=True,blank=True)
    description = models.TextField(null=True, blank=True)
    productImg = models.ImageField(upload_to=product_image_path, null=True, blank=True,)
    released_year = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return self.model
    
    

#------------------------------------------------- supplier model
class Supplier(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
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


# -------------------------------------------------- Inventory Model
class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, unique=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveIntegerField(null=True,blank=True)
    unit_cost = models.PositiveIntegerField()
    total_cost = models.PositiveBigIntegerField(null=True, blank=True)
    valuation = models.PositiveBigIntegerField(null=True, blank=True)
    profit = models.PositiveBigIntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.unit_cost
        if self.unit_price:
            product = Product.objects.get(id=self.product.id)
            if product:
                product.price = self.unit_price
            self.valuation = self.quantity * self.unit_price
            self.profit = self.valuation - self.total_cost
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.product.model


# ------------------------------------------------- Transaction Model
class Transaction(models.Model):
    # TRANSACTION_TYPE = [
    #     ('IN', 'IN'),
    #     ('OUT','OUT')
    # ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)
    transaction_type = models.CharField(max_length=5)
    payment_method = models.CharField(max_length=50,)
    amount = models.PositiveBigIntegerField()
    reference = models.CharField(max_length=100,null=True,blank=True)
    transaction_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.id


# -------------------------------------------------- Purchase Model
class Purchase(models.Model):
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

    category = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)

    quantity = models.PositiveIntegerField()
    unit_cost = models.PositiveIntegerField()

    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()

    transaction_type = models.CharField(null=True,blank=True,default='OUT')
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD)
    paid_ammount = models.PositiveBigIntegerField()
    reference = models.CharField(max_length=100,null=True,blank=True) 

    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['purchase_date']
    
    def __str__(self):
        return self.model



