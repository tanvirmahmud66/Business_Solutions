from django import forms
from .models import DeviceCategories

# ------------------------ Category Form
class CategoryForm(forms.Form):
    class Meta:
        model = DeviceCategories
        fields = '__all__'