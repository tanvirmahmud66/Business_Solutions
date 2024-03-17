from django import forms
from django.contrib.auth.forms import UserCreationForm
from multiupload.fields import MultiFileField
from .models import (
    User,
    Categories,
    Brand, 
    Inventory, 
    Product, 
    Supplier,
    Purchase
)

# ---------------------------------------Admin create Form
class AdminCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = User.objects.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)  # Ensure the proper database is used
        return user



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

class InventoryPriceSetForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['unit_price']

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
        fields = ['category','brand','model','quantity','unit_cost','supplier','payment_method','paid_ammount','reference']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 1})
        }
    


