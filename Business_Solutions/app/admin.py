from django.contrib import admin
from .models import Categories, Brand, Product, Inventory, Supplier, Transaction
# Register your models here.

class CategroyAdminView(admin.ModelAdmin):
    list_display = ('id', 'category')


class BrandAdminView(admin.ModelAdmin):
    list_display = ('id','brand')


class ProductAdminView(admin.ModelAdmin):
    list_display = ('id','category','brand','model','price','cost','description','released_year','created_at')


class InventoryAdminView(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity','supplierId','last_updated', 'created_at')


class TransactionAdminView(admin.ModelAdmin):
    list_display = ('id', 'product', 'transaction_type', 'payment_method', 'quantity','amount','transaction_code','transaction_date')


class SupplierAdminView(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'contact_person', 'email', 'phone_number','address','created_at')




admin.site.register(Categories, CategroyAdminView)
admin.site.register(Brand, BrandAdminView)
admin.site.register(Product,ProductAdminView)
admin.site.register(Inventory, InventoryAdminView)
admin.site.register(Supplier, SupplierAdminView)
admin.site.register(Transaction, TransactionAdminView)
