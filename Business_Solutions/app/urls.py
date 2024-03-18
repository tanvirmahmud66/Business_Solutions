from django.urls import path
from .views import DashboardView, InventoryView, CategoryListView,CreateCategoryView,StoreManageView, OrderView, ReportView
from .views import CreateBrandView, BrandListView, InventoryListView, ProductListView, CreateProductView, InventoryDetailsView, InventoryUpdateView, InventoryDeleteView

from .views import (

    AdminCreateView,
    AdminLoginView,
    AdminLogoutView,

    DashboardView,

    InventoryView,
    SalesListView,
    ClientUserView,
    InvoiceListView,
    InvoiceAddItem,

    InventoryListView,
    InventoryDetailsView,
    InventoryPriceSet,
    InventoryUpdateView,
    InventoryDeleteView,

    PurchaseListView,
    PurchaseCreateView,
    PurchaseDetailsView,
    PurchaseUpdateView,
    PurchaseDeleteView,

    ProductListView,
    CreateProductView,
    ProductDetailsView,
    ProductUpdateView,
    ProductDeleteView,

    CreateCategoryView,
    CategoryListView,
    CategoryUpdateView,
    CategoryDeleteView,

    CreateBrandView,
    BrandListView,
    BrandUpdateView,
    BrandDeleteView,

    SuppliersListView,
    SupplierCreateView,
    SupplierUpdateView,
    SupplierDeleteView,

)

urlpatterns = [

    path('',AdminLoginView.as_view(),name='admin-login'),
    path('signup/',AdminCreateView.as_view(),name='admin-signup'),
    path('logout/', AdminLogoutView.as_view(), name='admin-logout'),

    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('inventory/', InventoryView.as_view(), name='inventory'),
    path('inventory/sales-list/',SalesListView.as_view(),name='sales-list'),
    path('inventory/sales/new-sale/',ClientUserView.as_view(),name='new-sale'),
    path('inventory/sales/new-sale/<str:pk>/product-list/', InvoiceListView.as_view(),name='invoice-list'),
    path('inventory/sales/new-sale/<str:pk>/product-list/add-item/',InvoiceAddItem.as_view(),name='invoice-add-item'),

    path('inventory/inventory-list/', InventoryListView.as_view(), name='inventory-list'),
    path('inventory/<int:pk>/details/',InventoryDetailsView.as_view(),name='inventory-details'),
    path('inventory/<int:pk>/set-price/',InventoryPriceSet.as_view(),name='inventory-setPrice'),
    path('inventory/<int:pk>/update/',InventoryUpdateView.as_view(),name='inventory-update'),
    path('inventory/<int:pk>/delete/',InventoryDeleteView.as_view(),name='inventory-delete'),

    path('inventory/purchase/', PurchaseListView.as_view(),name='purchase-list'),
    path('inventory/purchase/new-purchase/',PurchaseCreateView.as_view(),name='new-purchase'),
    path('inventory/purchase/<int:pk>/details/',PurchaseDetailsView.as_view(),name='purchase-details'),
    path('inventory/purchase/<int:pk>/update/',PurchaseUpdateView.as_view(),name='purchase-update'),
    path('inventory/purchase/<int:pk>/delete/',PurchaseDeleteView.as_view(),name='purchase-delete'),

    path('inventory/product/product-list/', ProductListView.as_view(), name='product-list'),
    path('inventory/product/create-product/', CreateProductView.as_view(), name='create-product'),
    path('inventory/product/<int:pk>/details/', ProductDetailsView.as_view(), name='product-details'),
    path('inventory/product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('inventory/product/<int:pk>/delete/',ProductDeleteView.as_view(), name='product-delete'),

    path('inventory/category/category-list/',CategoryListView.as_view(),name='category-list'),
    path('inventory/category/create-category/', CreateCategoryView.as_view(), name='create-category'),
    path('inventory/category/<int:pk>/update/',CategoryUpdateView.as_view(),name='category-update'),
    path('inventory/category/<int:pk>/delete/',CategoryDeleteView.as_view(),name='category-delete'),

    path('inventory/brand/brand-list/', BrandListView.as_view(), name='brand-list'),
    path('inventory/brand/create-brand/', CreateBrandView.as_view(), name='create-brand'),
    path('inventory/brand/<int:pk>/update/', BrandUpdateView.as_view(), name='brand-update'),
    path('inventory/brand/<int:pk>/delete', BrandDeleteView.as_view(), name='brand-delete'),


    path('reports/', ReportView.as_view(), name='reports'),


    path('suppliers/', SuppliersListView.as_view(), name='supplier-list'),
    path('suppliers/create-supplier/',SupplierCreateView.as_view(), name='create-supplier'),
    path('suppliers/supplier/<int:pk>/update/',SupplierUpdateView.as_view(), name='supplier-update'),
    path('suppliers/supplier/<int:pk>/delete/',SupplierDeleteView.as_view(), name='supplier-delete'),


    path('orders/', OrderView.as_view(), name='orders'),


    path('manage-store/', StoreManageView.as_view(), name='manage'),

]