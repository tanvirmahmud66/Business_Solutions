from django import forms
from multiupload.fields import MultiFileField
from .models import (
    Categories,
    Brand, 
    Inventory, 
    Product, 
    Supplier,
    Purchase
)


# ------------------------ Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = '__all__'


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'


class Productform(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}), 
            'released_year': forms.SelectDateWidget(years=range(2018, 2030))
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 5}),
        }


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['category','brand','model','quantity','unit_cost','company_name','contact_person','email','phone_number','address','payment_method','paid_ammount','reference']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 1})
        }
    


