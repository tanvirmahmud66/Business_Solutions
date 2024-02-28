from django.contrib import admin
from .models import (
    Categories, 
    Brand, 
    Product, 
    Inventory, 
    Supplier,
    Transaction,
    Purchase
)
# Register your models here.

class CategroyAdminView(admin.ModelAdmin):
    list_display = ('id', 'category')


class BrandAdminView(admin.ModelAdmin):
    list_display = ('id','brand')


class ProductAdminView(admin.ModelAdmin):
    list_display = ('id','category','brand','model','cost','price','description','productImg','released_year','created_at')


class InventoryAdminView(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity','unit_price','unit_cost','total_cost','valuation','profit','last_updated', 'created_at')


class SupplierAdminView(admin.ModelAdmin):
    list_display = ('id', 'product','company_name', 'contact_person', 'email', 'phone_number','address','created_at')


class TransactionAdminView(admin.ModelAdmin):
    list_display = ('id','product','transaction_type','payment_method','amount','reference', 'transaction_date')


class PurchaseAdminView(admin.ModelAdmin):
    list_display = ('id','category','brand','model','quantity','unit_cost','company_name','contact_person','email','phone_number','address','transaction_type','payment_method','paid_ammount','reference','purchase_date')


admin.site.register(Categories, CategroyAdminView)
admin.site.register(Brand, BrandAdminView)
admin.site.register(Product,ProductAdminView)
admin.site.register(Inventory, InventoryAdminView)
admin.site.register(Supplier, SupplierAdminView)
admin.site.register(Transaction,TransactionAdminView)
admin.site.register(Purchase, PurchaseAdminView)