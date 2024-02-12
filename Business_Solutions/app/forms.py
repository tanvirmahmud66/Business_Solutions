from django import forms
from .models import DeviceCategories, Brand, Inventory, Device

# ------------------------ Category Form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = DeviceCategories
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
        model = Device
        fields = '__all__'