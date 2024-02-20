from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, DetailView, UpdateView
from django.views.generic.edit import DeleteView
from django.db.models import F, Sum
from django.db.models import Q
from .models import (
    Categories, 
    Brand, 
    Inventory, 
    Product, 
    Supplier, 
    Transaction,
    Purchase,
    Sale,
)
from .forms import (
    CategoryForm , 
    BrandForm, 
    InventoryForm, 
    Productform, 
    SupplierForm, 
    TransactionForm,
    PurchaseForm,
    SaleForm
)


class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'

# ==========================================INVENTORY SECTION=======================================
# ---------------------------------------------------------------Inventory View
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



# ---------------------------------------------------------------Sales list view
class SalesListView(ListView):
    model = Sale
    context_object_name = 'sales'
    template_name = 'inventory/sales/salesList.html'


# ---------------------------------------------------------------Sales create view
class SalesCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'inventory/sales/salesCreate.html'
    success_url = reverse_lazy('sales-list')

# ---------------------------------------------------------------Sales details view
class SalesDetailsView(DetailView):
    model = Sale
    context_object_name = 'sale'
    template_name = 'inventory/sales/salesDetails.html'


# ---------------------------------------------------------------Sales update view
class SalesUpdateView(UpdateView):
    model = Sale
    form_class = SaleForm
    context_object_name = 'sale'
    template_name = 'inventory/sales/salesUpdate.html'
    success_url = reverse_lazy('sales-list')


# ---------------------------------------------------------------Sales delete view
class SalesDeleteView(DeleteView):
    model = Sale
    context_object_name = 'sale'
    template_name = 'inventory/sales/salesDelete.html'
    success_url = reverse_lazy('sales-list')


# ---------------------------------------------------------------Inventory list view
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

        return queryset
    

# ---------------------------------------------------------------Inventory create view
class CreateInventoryView(CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory/addInventory.html'

    def get_success_url(self):
        return reverse('inventory-list')

## ---------------------------------------------------------------Inventory detail view
class InventoryDetailsView(DetailView):
    model = Inventory
    template_name = 'inventory/inventoryDetails.html'
    context_object_name = 'inventory'

# ---------------------------------------------------------------Inventory Update view
class InventoryUpdateView(UpdateView):
    model = Inventory
    form_class = InventoryForm
    context_object_name = 'inventory'
    template_name = 'inventory/inventoryUpdate.html'

    def get_success_url(self):
        return reverse('inventory-details',kwargs={'pk': self.object.pk})

# ---------------------------------------------------------------Inventory delete view
class InventoryDeleteView(DeleteView):
    model = Inventory
    template_name = 'inventory/inventoryDelete.html'
    context_object_name = 'inventory'
    success_url = reverse_lazy('inventory-list')


# ---------------------------------------------------------------Purchase list View
class PurchaseListView(ListView):
    model = Purchase
    context_object_name = 'purchases'
    template_name = 'inventory/purchase/purchaseList.html'

# ---------------------------------------------------------------Purchase create View
class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'inventory/purchase/purchaseCreate.html'
    success_url = reverse_lazy('purchase-list')

# ---------------------------------------------------------------Purchase detail View
class PurchaseDetailsView(DetailView):
    model = Purchase
    context_object_name = 'purchase'
    template_name = 'inventory/purchase/purchaseDetails.html'

# ---------------------------------------------------------------Purchase update View
class PurchaseUpdateView(UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'inventory/purchase/purchaseUpdate.html'
    success_url = reverse_lazy('purchase-list')

# ---------------------------------------------------------------Purchase update View
class PurchaseDeleteView(DeleteView):
    model = Purchase
    context_object_name = 'purchase'
    template_name = 'inventory/purchase/purchaseDelete.html'
    success_url = reverse_lazy('purchase-list')

# ---------------------------------------------------------------product list View
class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'inventory/productList.html'
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
            queryset = queryset.filter(model__icontains=search_query)

        if cate:
            queryset = queryset.filter(category__id=cate)
        if brand:
            queryset = queryset.filter(brand__id=brand)
        if price:
            queryset = queryset.filter(price__gte=price)

        if brand and cate and price==None:
            queryset = queryset.filter(
                 Q(brand__id=brand) &
                 Q(category__id=cate)
            )
        elif price and cate and brand==None:
            queryset = queryset.filter(
                 Q(price__gte=price) &
                 Q(category__id=cate)
            )
        elif price and brand and cate==None:
            queryset = queryset.filter(
                 Q(price__gte=price) &
                 Q(brand__id=brand)
            )
        elif price and brand and cate:
            queryset = queryset.filter(
                 Q(price__gte=price) &
                 Q(brand__id=brand) &
                 Q(category__id=cate)
            )
            
        return queryset


# ---------------------------------------------------------------Product create view
class CreateProductView(CreateView):
    model = Product
    form_class = Productform
    template_name = 'inventory/addProduct.html'

    def get_success_url(self):
        return reverse('product-list')
    
# ---------------------------------------------------------------Product Details view
class ProductDetailsView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'inventory/productDetails.html'

# ---------------------------------------------------------------Product update view
class ProductUpdateView(UpdateView):
    model = Product
    form_class = Productform
    context_object_name = 'product'
    template_name = 'inventory/productUpdate.html'

    def get_success_url(self):
        return reverse('product-details',kwargs={'pk': self.object.pk})

# ---------------------------------------------------------------Product Delete View
class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = 'product'
    template_name = 'inventory/productDelete.html'
    success_url = reverse_lazy('product-list')


# ---------------------------------------------------------------Category Create view
class CreateCategoryView(CreateView):
    model = Categories
    form_class = CategoryForm
    template_name = 'inventory/addCategory.html'

    def get_success_url(self):
        return reverse('category-list')

# ---------------------------------------------------------------Categroy list view
class CategoryListView(ListView):
    model = Categories
    context_object_name = 'categories'
    template_name = 'inventory/allcategory.html'

# ---------------------------------------------------------------Category Update view
class CategoryUpdateView(UpdateView):
    model = Categories
    form_class = CategoryForm
    context_object_name = 'category'
    template_name = 'inventory/categoryUpdate.html'
    success_url = reverse_lazy('category-list')

# ---------------------------------------------------------------Category Delete view
class CategoryDeleteView(DeleteView):
    model = Categories
    context_object_name = 'category'
    template_name = 'inventory/categoryDelete.html'
    success_url = reverse_lazy('category-list')


# ---------------------------------------------------------------Brand list view
class BrandListView(ListView):
    model = Brand
    context_object_name = 'brands'
    template_name = 'inventory/brandList.html'

# ---------------------------------------------------------------Brand create view
class CreateBrandView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'inventory/addbrand.html'

    def get_success_url(self):
        return reverse('brand-list')
    
# ---------------------------------------------------------------Brand update view
class BrandUpdateView(UpdateView):
    model = Brand
    form_class = BrandForm
    context_object_name = 'brand'
    template_name = 'inventory/brandUpdate.html'
    success_url = reverse_lazy('brand-list')

# ---------------------------------------------------------------Brand Delete view
class BrandDeleteView(DeleteView):
    model = Brand
    context_object_name = 'brand'
    template_name = 'inventory/brandDelete.html'
    success_url = reverse_lazy('brand-list')





# ==========================================REPORT SECTION=======================================
class ReportView(TemplateView):
    template_name = 'reports/index.html'

# ==========================================SUPPLIERS SECTION=======================================
# ---------------------------------------------------------------Supplier List view
class SuppliersListView(ListView):
    model = Supplier
    context_object_name = 'suppliers'
    template_name = 'suppliers/supplierList.html'

# ---------------------------------------------------------------Supplier create view
class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplierCreate.html'
    success_url = reverse_lazy('supplier-list')

# ---------------------------------------------------------------Supplier update view
class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    context_object_name = 'supplier'
    template_name = 'suppliers/supplierUpdate.html'
    success_url = reverse_lazy('supplier-list')

# ---------------------------------------------------------------Supplier delete view
class SupplierDeleteView(DeleteView):
    model = Supplier
    form_class = SupplierForm
    context_object_name = 'supplier'
    template_name = 'suppliers/supplierDelete.html'
    success_url = reverse_lazy('supplier-list')

# ==========================================ORDER SECTION=======================================
class OrderView(TemplateView):
    template_name = 'orders/index.html'

# ==========================================MANAGE STORE SECTION=======================================
class StoreManageView(TemplateView):
    template_name = 'manage/index.html'