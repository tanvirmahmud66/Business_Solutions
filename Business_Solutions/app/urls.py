from django.urls import path
from .views import DashboardView, InventoryView, CategoryListView,CreateCategoryView,StoreManageView, OrderView, ReportView, SuppliersView
from .views import CreateBrandView, BrandListView, InventoryListView, ProductListView, CreateInventoryView, CreateProductView
urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),


    path('inventory/', InventoryView.as_view(), name='inventory'),
    path('inventory/all-inventory/', InventoryListView.as_view(), name='inventory-list'),
    path('inventory/all-product/', ProductListView.as_view(), name='product-list'),
    path('inventory/all-category/',CategoryListView.as_view(),name='all-category'),
    path('inventory/all-brand/', BrandListView.as_view(), name='all-brand'),
    path('inventory/create-inventory/', CreateInventoryView.as_view(), name='create-inventory'),
    path('inventory/create-product/', CreateProductView.as_view(), name='create-product'),
    path('inventory/create-category/', CreateCategoryView.as_view(), name='create-category'),
    path('inventory/create-brand/', CreateBrandView.as_view(), name='create-brand'),


    path('reports/', ReportView.as_view(), name='reports'),


    path('suppliers/', SuppliersView.as_view(), name='suppliers'),


    path('orders/', OrderView.as_view(), name='orders'),


    path('manage-store/', StoreManageView.as_view(), name='manage'),

]