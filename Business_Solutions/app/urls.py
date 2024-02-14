from django.urls import path
from .views import DashboardView, InventoryView, CategoryListView,CreateCategoryView,StoreManageView, OrderView, ReportView, SuppliersView
from .views import CreateBrandView, BrandListView, InventoryListView, ProductListView, CreateInventoryView, CreateProductView, InventoryDetailsView, InventoryUpdateView, InventoryDeleteView


urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),


    path('inventory/', InventoryView.as_view(), name='inventory'),
    path('inventory/inventory-list/', InventoryListView.as_view(), name='inventory-list'),
    path('inventory/create-inventory/', CreateInventoryView.as_view(), name='create-inventory'),
    path('inventory/<int:pk>/details/',InventoryDetailsView.as_view(),name='inventory-details'),
    path('inventory/<int:pk>/update/',InventoryUpdateView.as_view(),name='inventory-update'),
    path('inventory/<int:pk>/delete/',InventoryDeleteView.as_view(),name='inventory-delete'),
    path('inventory/product/product-list/', ProductListView.as_view(), name='product-list'),
    path('inventory/product/create-product/', CreateProductView.as_view(), name='create-product'),
    path('inventory/category/category-list/',CategoryListView.as_view(),name='category-list'),
    path('inventory/category/create-category/', CreateCategoryView.as_view(), name='create-category'),
    path('inventory/brand/brand-list/', BrandListView.as_view(), name='brand-list'),
    path('inventory/brand/create-brand/', CreateBrandView.as_view(), name='create-brand'),


    path('reports/', ReportView.as_view(), name='reports'),


    path('suppliers/', SuppliersView.as_view(), name='suppliers'),


    path('orders/', OrderView.as_view(), name='orders'),


    path('manage-store/', StoreManageView.as_view(), name='manage'),

]