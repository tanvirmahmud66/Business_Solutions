from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView

from .models import DeviceCategories, Brand, Inventory, Device
from .forms import CategoryForm , BrandForm, InventoryForm, Productform
# Create your views here.

# def count_records(Model,id):
#     count = Model.objects.filter(id=id).count()
#     return count


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

# ----------------------------------------------------------------------INVENTORY SECTION
class InventoryView(ListView):
    template_name = 'inventory/inventory.html'
    context_object_name = 'data'
    count_list = []
    category_model = DeviceCategories.objects.all()
    for each in category_model:
        cate = each.category
        count = Device.objects.filter(category__id=each.id).count()
        count_list.append({f"{cate}":count})
    print(count_list)
    extra_context = {
        'counts': count_list,
    }

    def get_queryset(self):
        inventories = Inventory.objects.all().order_by('-id')[:5]
        products = Device.objects.all().order_by('-id')[:5]
        categories = DeviceCategories.objects.all().order_by('id')[:5]
        brands = Brand.objects.all().order_by('id')[:5]
        return {
            'inventories': inventories,
            'products': products,
            'categories': categories,
            'brands': brands,
        }

class InventoryListView(ListView):
    model = Inventory
    context_object_name = 'inventories'
    template_name = 'inventory/inventoryList.html'

class ProductListView(ListView):
    model = Device
    context_object_name = 'products'
    template_name = 'inventory/productList.html'

class CategoryListView(ListView):
    model = DeviceCategories
    context_object_name = 'categories'
    template_name = 'inventory/allcategory.html'
    


class BrandListView(ListView):
    model = Brand
    context_object_name = 'brands'
    template_name = 'inventory/brandList.html'


class CreateInventoryView(CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory/addInventory.html'

    def get_success_url(self):
        return reverse('inventory-list')


class CreateProductView(CreateView):
    model = Device
    form_class = Productform
    template_name = 'inventory/addProduct.html'

    def get_success_url(self):
        return reverse('product-list')


class CreateCategoryView(CreateView):
    model = DeviceCategories
    form_class = CategoryForm
    template_name = 'inventory/addCategory.html'

    def get_success_url(self):
        return reverse('all-category')


class CreateBrandView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'inventory/addbrand.html'

    def get_success_url(self):
        return reverse('all-brand')






class ReportView(TemplateView):
    template_name = 'reports/index.html'


class SuppliersView(TemplateView):
    template_name = 'suppliers/index.html'


class OrderView(TemplateView):
    template_name = 'orders/index.html'


class StoreManageView(TemplateView):
    template_name = 'manage/index.html'