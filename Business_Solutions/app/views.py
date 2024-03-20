from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from django.shortcuts import redirect
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import DeleteView
from django.db.models import Q
from django.db.models import Sum
from django.views.generic import (
    FormView,
    TemplateView, 
    ListView, 
    CreateView, 
    DetailView, 
    UpdateView
)
from .models import (
    User,
    Categories, 
    Brand, 
    Inventory, 
    Product, 
    Supplier,
    Purchase,
    Transaction,
    GeneralUser, 
    ProductLineUp,
    Sales
)
from .forms import (
    AdminCreateForm,
    CategoryForm , 
    BrandForm, 
    InventoryForm,
    InventoryPriceSetForm,
    Productform, 
    SupplierForm,
    PurchaseForm,
    GeneralUserForm,
    ProductLineUpForm,
    SalesForm
)

# =========================================AUTHENTICATION SECTION===================================
# ----------------------------------------------------Permission Mixin
class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser
    
# -------------------------------------------------Admin singup view
class AdminCreateView(CreateView):
    template_name = 'authentication/singup.html'
    form_class = AdminCreateForm
    success_url = reverse_lazy('dashboard')


# -------------------------------------------------Admin login view
class AdminLoginView(LoginView):
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('dashboard')

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('dashboard')
        else:
            print("User is not staff")
            return reverse_lazy('admin-login')


# ----------------------------------------------------------Admin login view
class AdminLogoutView(SuperuserRequiredMixin, LogoutView):
    next_page = reverse_lazy('admin-login')
        


# =========================================DASHBOARD SECTION========================================
class DashboardView(SuperuserRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'


# ==========================================INVENTORY SECTION=======================================
# ---------------------------------------------------------------Inventory View
class InventoryView(SuperuserRequiredMixin,ListView):
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


# --------------------------------------------------------------- Sales List View
class SalesListView(TemplateView):
    template_name = 'inventory/sales/salesList.html'


# --------------------------------------------------------------- General user create view
class ClientUserView(SuperuserRequiredMixin, CreateView):
    model = GeneralUser
    form_class = GeneralUserForm
    template_name = 'inventory/sales/createClientUser.html'

    def get_success_url(self):
        return reverse('invoice-list',kwargs={'pk': self.object.email})
    
    def form_valid(self, form):
        self.first_name = form.cleaned_data['first_name']
        self.last_name = form.cleaned_data['last_name']
        self.email = form.cleaned_data['email']
        self.phone = form.cleaned_data['phone']

        if self.email:
            user = User.objects.filter(email=self.email).first()
            if user:
                return redirect('invoice-list', pk=self.email)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        email = form.data['email']
        general_user = GeneralUser.objects.filter(email=email).first()
        if general_user:
            return redirect('invoice-list', pk=form.data['email'])
        return super().form_invalid(form)
    
    
    

# --------------------------------------------------------------- invoice list
class InvoiceListView(SuperuserRequiredMixin, ListView):
    model = ProductLineUp
    template_name = 'inventory/sales/invoiceList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_list = ProductLineUp.objects.filter(token = self.kwargs.get('pk'), sale_confirm=False)
        context['product_list'] = product_list
        total_amount = product_list.aggregate(total_amount=Sum('subtotal'))['total_amount']
        context['total_amount'] = total_amount
        pk = self.kwargs.get('pk')
        print(pk)
        if pk:
            if User.objects.filter(email=pk).exists():
                context['buyer'] = User.objects.filter(email=pk).first()
            if GeneralUser.objects.filter(email=pk).exists():
                context['buyer'] = GeneralUser.objects.filter(email=pk).first()
        return context


# ---------------------------------------------------------------- invoice add item
class InvoiceAddItem(SuperuserRequiredMixin, CreateView):
    model = ProductLineUp
    form_class = ProductLineUpForm
    template_name = 'inventory/sales/invoiceAddItem.html'

    def get_success_url(self):
        return reverse('invoice-list',kwargs={'pk': self.kwargs.get('pk', None)})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.kwargs.get('pk',None)
        return context
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        token_param = self.kwargs.get('pk', None)
        obj.token = token_param
        obj.subtotal = obj.quantity * obj.product.unit_price
        obj.save()
        return super().form_valid(form)


#----------------------------------------------------------------- invoice remove item
class InvoiceRemoveItem(SuperuserRequiredMixin, DeleteView):
    model = ProductLineUp
    context_object_name = 'invoiceItem'
    template_name = 'inventory/sales/invoiceRemoveItem.html'

    def get_success_url(self):
        return reverse('invoice-list',kwargs={'pk': self.kwargs.get('email', None)})   




# ---------------------------------------------------------------Inventory list view
class InventoryListView(SuperuserRequiredMixin,ListView):
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
class InventoryDetailsView(SuperuserRequiredMixin,DetailView):
    model = Inventory
    template_name = 'inventory/inventoryDetails.html'
    context_object_name = 'inventory'


#---------------------------------------------------------------- Inventory Priduct price set
class InventoryPriceSet(SuperuserRequiredMixin,UpdateView):
    model = Inventory
    form_class = InventoryPriceSetForm
    context_object_name = 'inventory'
    template_name = 'inventory/inventorySetPrice.html'
    success_url = reverse_lazy('inventory-list')

    def form_valid(self, form):
        self.unit_price = form.cleaned_data['unit_price']
        product = Product.objects.get(id=self.object.product.id)
        if product:
            product.price = self.unit_price
            product.save()
        return super().form_valid(form)


# ---------------------------------------------------------------Inventory Update view
class InventoryUpdateView(SuperuserRequiredMixin,UpdateView):
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
class InventoryDeleteView(SuperuserRequiredMixin,DeleteView):
    model = Inventory
    template_name = 'inventory/inventoryDelete.html'
    context_object_name = 'inventory'
    success_url = reverse_lazy('inventory-list')



#----------------------------------------------------------------Purchase list view
class PurchaseListView(SuperuserRequiredMixin,ListView):
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
class PurchaseCreateView(SuperuserRequiredMixin,CreateView):
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
class PurchaseDetailsView(SuperuserRequiredMixin,DetailView):
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
class PurchaseUpdateView(SuperuserRequiredMixin,UpdateView):
    model = Purchase
    form_class = PurchaseForm
    context_object_name = 'purchase'
    template_name = 'inventory/purchase/purchaseUpdate.html'

    def get_success_url(self):
        return reverse('purchase-details',kwargs={'pk': self.object.pk})
    


# --------------------------------------------------------------- Purchase details view
class PurchaseDeleteView(SuperuserRequiredMixin,DeleteView):
    model = Purchase
    context_object_name = 'purchase'
    template_name = 'inventory/purchase/purchaseDelete.html'
    success_url = reverse_lazy('purchase-list')

# ---------------------------------------------------------------product list View
class ProductListView(SuperuserRequiredMixin,ListView):
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
class CreateProductView(SuperuserRequiredMixin,CreateView):
    model = Product
    form_class = Productform
    template_name = 'inventory/product/addProduct.html'

    def get_success_url(self):
        return reverse('product-list')
    
# ---------------------------------------------------------------Product Details view
class ProductDetailsView(SuperuserRequiredMixin,DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'inventory/product/productDetails.html'

# ---------------------------------------------------------------Product update view
class ProductUpdateView(SuperuserRequiredMixin,UpdateView):
    model = Product
    form_class = Productform
    context_object_name = 'product'
    template_name = 'inventory/product/productUpdate.html'

    def get_success_url(self):
        return reverse('product-details',kwargs={'pk': self.object.pk})


# ---------------------------------------------------------------Product Delete View
class ProductDeleteView(SuperuserRequiredMixin,DeleteView):
    model = Product
    context_object_name = 'product'
    template_name = 'inventory/product/productDelete.html'
    success_url = reverse_lazy('product-list')


# ---------------------------------------------------------------Category Create view
class CreateCategoryView(SuperuserRequiredMixin,CreateView):
    model = Categories
    form_class = CategoryForm
    template_name = 'inventory/category/addCategory.html'

    def get_success_url(self):
        return reverse('category-list')


# ---------------------------------------------------------------Categroy list view
class CategoryListView(SuperuserRequiredMixin,ListView):
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
class CategoryUpdateView(SuperuserRequiredMixin,UpdateView):
    model = Categories
    form_class = CategoryForm
    context_object_name = 'category'
    template_name = 'inventory/category/categoryUpdate.html'
    success_url = reverse_lazy('category-list')


# ---------------------------------------------------------------Category Delete view
class CategoryDeleteView(SuperuserRequiredMixin,DeleteView):
    model = Categories
    context_object_name = 'category'
    template_name = 'inventory/category/categoryDelete.html'
    success_url = reverse_lazy('category-list')


# ---------------------------------------------------------------Brand list view
class BrandListView(SuperuserRequiredMixin,ListView):
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
class CreateBrandView(SuperuserRequiredMixin,CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'inventory/brand/addbrand.html'

    def get_success_url(self):
        return reverse('brand-list')


# ---------------------------------------------------------------Brand update view
class BrandUpdateView(SuperuserRequiredMixin,UpdateView):
    model = Brand
    form_class = BrandForm
    context_object_name = 'brand'
    template_name = 'inventory/brand/brandUpdate.html'
    success_url = reverse_lazy('brand-list')


# ---------------------------------------------------------------Brand Delete view
class BrandDeleteView(SuperuserRequiredMixin,DeleteView):
    model = Brand
    context_object_name = 'brand'
    template_name = 'inventory/brand/brandDelete.html'
    success_url = reverse_lazy('brand-list')





# ==========================================REPORT SECTION=======================================
class ReportView(SuperuserRequiredMixin,TemplateView):
    template_name = 'reports/index.html'

# ==========================================SUPPLIERS SECTION=======================================
# ---------------------------------------------------------------Supplier List view
class SuppliersListView(SuperuserRequiredMixin,ListView):
    model = Supplier
    context_object_name = 'suppliers'
    template_name = 'suppliers/supplierList.html'

# ---------------------------------------------------------------Supplier create view
class SupplierCreateView(SuperuserRequiredMixin,CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/supplierCreate.html'
    success_url = reverse_lazy('supplier-list')

# ---------------------------------------------------------------Supplier update view
class SupplierUpdateView(SuperuserRequiredMixin,UpdateView):
    model = Supplier
    form_class = SupplierForm
    context_object_name = 'supplier'
    template_name = 'suppliers/supplierUpdate.html'
    success_url = reverse_lazy('supplier-list')

# ---------------------------------------------------------------Supplier delete view
class SupplierDeleteView(SuperuserRequiredMixin,DeleteView):
    model = Supplier
    form_class = SupplierForm
    context_object_name = 'supplier'
    template_name = 'suppliers/supplierDelete.html'
    success_url = reverse_lazy('supplier-list')

# ==========================================ORDER SECTION=======================================
class OrderView(SuperuserRequiredMixin,TemplateView):
    template_name = 'orders/index.html'

# ==========================================MANAGE STORE SECTION=======================================
class StoreManageView(SuperuserRequiredMixin,TemplateView):
    template_name = 'manage/index.html'