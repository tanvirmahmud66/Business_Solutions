from django.shortcuts import redirect
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.db import IntegrityError
from datetime import datetime
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
    Purchase,
    Transaction,
)
from .forms import (
    CategoryForm , 
    BrandForm, 
    InventoryForm, 
    Productform, 
    SupplierForm,
    PurchaseForm,
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

        return {
            'inventories': inventories,
            'products': products,
            'categories': categories,
            'brands': brands,
        }


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
    
    def form_valid(self, form):
        self.unit_price = form.cleaned_data['unit_price']
        self.unit_cost = form.cleaned_data['unit_cost']
        product = Product.objects.get(id=self.object.product.id)
        if product:
            product.cost = self.unit_cost
            product.price = self.unit_price
            product.save()
        return super().form_valid(form)



# ---------------------------------------------------------------Inventory delete view
class InventoryDeleteView(DeleteView):
    model = Inventory
    template_name = 'inventory/inventoryDelete.html'
    context_object_name = 'inventory'
    success_url = reverse_lazy('inventory-list')



#----------------------------------------------------------------Purchase list view
class PurchaseListView(ListView):
    model = Purchase
    context_object_name = 'purchases'
    template_name = 'inventory/purchase/purchaseList.html'
    categories = Categories.objects.all()
    brand = Brand.objects.all()
    supplier = Supplier.objects.all()
    extra_context = {
        'categories': categories,
        'brands': brand,
        'suppliers': supplier,
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', None)
        category = self.request.GET.get('category', None)
        brand = self.request.GET.get('brand',None)
        supplier = self.request.GET.get('supplier',None)
        purchase_date = self.request.GET.get('purchase_date',None)

        if search_query:
            queryset = queryset.filter(model__icontains=search_query)

        if category:
            queryset = queryset.filter(category=category)
        if brand:
            queryset = queryset.filter(brand=brand)
        if supplier:
            queryset = queryset.filter(supplier=supplier)
        if purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(Q(purchase_date__date=date_object))

        if category and brand and supplier==None and purchase_date==None:
            queryset = queryset.filter(
                Q(category=category) &
                Q(brand=brand)
            )
        elif category and brand==None and supplier and purchase_date==None:
            queryset = queryset.filter(
                Q(category=category) &
                Q(supplier=supplier)
            )
        elif category and brand==None and supplier==None and purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(category=category) &
                Q(purchase_date__date=date_object)
            )
        elif category==None and brand and supplier and purchase_date==None:
            queryset = queryset.filter(
                Q(brand=brand) &
                Q(supplier=supplier)
            )
        elif category==None and brand and supplier==None and purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(brand=brand) &
                Q(purchase_date__date=date_object)
            )
        elif category==None and brand==None and supplier and purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(supplier=supplier) &
                Q(purchase_date__date=date_object)
            )
        elif category and brand and supplier and purchase_date==None:
            queryset = queryset.filter(
                Q(category=category) &
                Q(brand=brand) &
                Q(supplier=supplier)
            )
        elif category and brand and supplier==None and purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(category=category) &
                Q(brand=brand) &
                Q(purchase_date__date=date_object)
            )
        elif category and brand==None and supplier and purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(category=category) &
                Q(supplier=supplier) &
                Q(purchase_date__date=date_object)
            )
        elif category==None and brand and supplier and purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(brand=brand) &
                Q(supplier=supplier) &
                Q(purchase_date__date=date_object)
            )
        elif category and brand and supplier and purchase_date:
            date_object = datetime.strptime(purchase_date, "%Y-%m-%d").date()
            queryset = queryset.filter(
                Q(category=category) &
                Q(brand=brand) &
                Q(supplier=supplier) &
                Q(purchase_date__date=date_object)
            )

        return queryset


# --------------------------------------------------------------- new Purchase view
class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'inventory/purchase/newPurchase.html'
    success_url = reverse_lazy('purchase-list')

    def form_valid(self, form):
        category = form.cleaned_data['category']
        brand = form.cleaned_data['brand']
        model = form.cleaned_data['model']
        quantity = form.cleaned_data['quantity']
        unit_cost = form.cleaned_data['unit_cost']
        payment_method = form.cleaned_data['payment_method']
        paid_ammount = form.cleaned_data['paid_ammount']
        reference = form.cleaned_data['reference']

        if not Product.objects.filter(category=category, brand=brand, model=model).exists():
            self.new_product = Product.objects.create(category=category, brand=brand, model=model, cost=unit_cost)
            self.new_product.save()
        else:
            self.new_product = Product.objects.get(category=category, brand=brand, model=model)

        if Inventory.objects.filter(product=self.new_product).exists():
            self.get_inventory = Inventory.objects.get(product=self.new_product)
            self.get_inventory.quantity += quantity
            self.get_inventory.save()
        else:
            self.new_inventory = Inventory.objects.create(
                product=self.new_product,
                quantity=quantity,
                unit_cost=unit_cost,
            )
            self.new_inventory.save()
        
        self.object = form.save()

        self.new_transaction = Transaction.objects.create(
            product=self.new_product,
            transaction_type = "OUT",
            payment_method=payment_method,
            amount = paid_ammount,
            reference = reference,
            transaction_date = self.object.purchase_date
        )        
        return super().form_valid(form)


# --------------------------------------------------------------- Purchase details view
class PurchaseDetailsView(DetailView):
    model = Purchase
    context_object_name = 'purchase'
    template_name = 'inventory/purchase/purchaseDetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase = self.get_object()
        supplier = purchase.supplier
        context['supplier'] = supplier
        return context


# --------------------------------------------------------------- Purchase details view
class PurchaseUpdateView(UpdateView):
    model = Purchase
    form_class = PurchaseForm
    context_object_name = 'purchase'
    template_name = 'inventory/purchase/purchaseUpdate.html'

    def get_success_url(self):
        return reverse('purchase-details',kwargs={'pk': self.object.pk})
    


# --------------------------------------------------------------- Purchase details view
class PurchaseDeleteView(DeleteView):
    model = Purchase
    context_object_name = 'purchase'
    template_name = 'inventory/purchase/purchaseDelete.html'
    success_url = reverse_lazy('purchase-list')

# ---------------------------------------------------------------product list View
class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'inventory/product/productList.html'
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
    template_name = 'inventory/product/addProduct.html'

    def get_success_url(self):
        return reverse('product-list')
    
# ---------------------------------------------------------------Product Details view
class ProductDetailsView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'inventory/product/productDetails.html'

# ---------------------------------------------------------------Product update view
class ProductUpdateView(UpdateView):
    model = Product
    form_class = Productform
    context_object_name = 'product'
    template_name = 'inventory/product/productUpdate.html'

    def get_success_url(self):
        return reverse('product-details',kwargs={'pk': self.object.pk})

# ---------------------------------------------------------------Product Delete View
class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = 'product'
    template_name = 'inventory/product/productDelete.html'
    success_url = reverse_lazy('product-list')


# ---------------------------------------------------------------Category Create view
class CreateCategoryView(CreateView):
    model = Categories
    form_class = CategoryForm
    template_name = 'inventory/category/addCategory.html'

    def get_success_url(self):
        return reverse('category-list')

# ---------------------------------------------------------------Categroy list view
class CategoryListView(ListView):
    model = Categories
    context_object_name = 'categories'
    template_name = 'inventory/category/allcategory.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(category__icontains=search_query)
        return queryset

# ---------------------------------------------------------------Category Update view
class CategoryUpdateView(UpdateView):
    model = Categories
    form_class = CategoryForm
    context_object_name = 'category'
    template_name = 'inventory/category/categoryUpdate.html'
    success_url = reverse_lazy('category-list')

# ---------------------------------------------------------------Category Delete view
class CategoryDeleteView(DeleteView):
    model = Categories
    context_object_name = 'category'
    template_name = 'inventory/category/categoryDelete.html'
    success_url = reverse_lazy('category-list')


# ---------------------------------------------------------------Brand list view
class BrandListView(ListView):
    model = Brand
    context_object_name = 'brands'
    template_name = 'inventory/brand/brandList.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(brand__icontains=search_query)
        return queryset

# ---------------------------------------------------------------Brand create view
class CreateBrandView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'inventory/brand/addbrand.html'

    def get_success_url(self):
        return reverse('brand-list')
    
# ---------------------------------------------------------------Brand update view
class BrandUpdateView(UpdateView):
    model = Brand
    form_class = BrandForm
    context_object_name = 'brand'
    template_name = 'inventory/brand/brandUpdate.html'
    success_url = reverse_lazy('brand-list')

# ---------------------------------------------------------------Brand Delete view
class BrandDeleteView(DeleteView):
    model = Brand
    context_object_name = 'brand'
    template_name = 'inventory/brand/brandDelete.html'
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