from django.urls import path
from .views import DashboardView, InventoryView, StoreManageView, OrderView, ReportView, SuppliersView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),


    path('inventory/', InventoryView.as_view(), name='inventory'),


    path('reports/', ReportView.as_view(), name='reports'),


    path('suppliers/', SuppliersView.as_view(), name='suppliers'),


    path('orders/', OrderView.as_view(), name='orders'),


    path('manage-store/', InventoryView.as_view(), name='manage'),

]