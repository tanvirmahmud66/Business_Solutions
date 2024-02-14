from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView
from django.views.generic.edit import DeleteView
from django.db.models import F, Sum
from django.db.models import Q
from .models import Categories, Brand, Inventory, Product, Supplier, Transaction
from .forms import CategoryForm , BrandForm, InventoryForm, Productform, SupplierForm, TransactionForm
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

    def get_queryset(self):
        categories = Categories.objects.all().order_by('id')[:5]
        brands = Brand.objects.all().order_by('id')[:5]
        products = Product.objects.all().order_by('-id')[:5]
        inventories = Inventory.objects.all().order_by('-id')[:5]
        transactions = Transaction.objects.all().order_by('-id')[:5]

        return {
            'inventories': inventories,
            'products': products,
            'categories': categories,
            'brands': brands,
            'transactions':transactions,
        }


class InventoryListView(ListView):
    model = Inventory
    context_object_name = 'inventories'
    template_name = 'inventory/inventoryList.html'
    categories_model = Categories.objects.all()
    brand_model = Brand.objects.all()
    extra_context = {
        'categories': categories_model,
        'brands': brand_model
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', None)
        cate = self.request.GET.get('category', None)
        brand = self.request.GET.get('brand',None)
        price = self.request.GET.get('price',None)
        if search_query:
            queryset = queryset.filter(product__model__icontains=search_query)

        if cate:
            queryset = queryset.filter(product__category__id=cate)
        if brand:
            queryset = queryset.filter(product__brand__id=brand)
        if price:
            queryset = queryset.filter(product__price__gte=price)

        if brand and cate and price==None:
            queryset = queryset.filter(
                 Q(product__brand__id=brand) &
                 Q(product__category__id=cate)
            )
        elif price and cate and brand==None:
            queryset = queryset.filter(
                 Q(product__price__gte=price) &
                 Q(product__category__id=cate)
            )
        elif price and brand and cate==None:
            queryset = queryset.filter(
                 Q(product__price__gte=price) &
                 Q(product__brand__id=brand)
            )
        elif price and brand and cate:
            queryset = queryset.filter(
                 Q(product__price__gte=price) &
                 Q(product__brand__id=brand) &
                 Q(product__category__id=cate)
            )

        queryset = queryset.annotate(total_value=F('quantity') * F('product__price'))
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_value_sum = self.get_queryset().aggregate(Sum('total_value'))['total_value__sum']
        context['total_value_sum'] = total_value_sum

        return context


class CreateInventoryView(CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory/addInventory.html'

    def get_success_url(self):
        return reverse('inventory-list')


class InventoryDetailsView(DetailView):
    model = Inventory
    template_name = 'inventory/inventoryDetails.html'
    context_object_name = 'inventory'


class InventoryUpdateView(UpdateView):
    model = Inventory
    form_class = InventoryForm
    context_object_name = 'inventory'
    template_name = 'inventory/inventoryUpdate.html'

    def get_success_url(self):
        return reverse('inventory-details',kwargs={'pk': self.object.pk})


class InventoryDeleteView(DeleteView):
    model = Inventory
    template_name = 'inventory/inventoryDelete.html'
    context_object_name = 'inventory'
    success_url = reverse_lazy('inventory-list')



class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'inventory/productList.html'

    

class CategoryListView(ListView):
    model = Categories
    context_object_name = 'categories'
    template_name = 'inventory/allcategory.html'
    


class BrandListView(ListView):
    model = Brand
    context_object_name = 'brands'
    template_name = 'inventory/brandList.html'





class CreateProductView(CreateView):
    model = Product
    form_class = Productform
    template_name = 'inventory/addProduct.html'

    def get_success_url(self):
        return reverse('product-list')


class CreateCategoryView(CreateView):
    model = Categories
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