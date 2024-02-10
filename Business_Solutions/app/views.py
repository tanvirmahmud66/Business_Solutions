from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from .models import DeviceCategories
from .forms import CategoryForm 
# Create your views here.

class DashboardView(TemplateView):
    template_name = 'dashboard/index.html'


class InventoryView(ListView):
    model = DeviceCategories
    template_name = 'inventory/index.html'
    context_object_name = 'Categories'


class ReportView(TemplateView):
    template_name = 'reports/index.html'


class SuppliersView(TemplateView):
    template_name = 'suppliers/index.html'


class OrderView(TemplateView):
    template_name = 'orders/index.html'


class StoreManageView(TemplateView):
    template_name = 'manage/index.html'