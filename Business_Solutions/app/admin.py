from django.contrib import admin
from .models import DeviceCategories, Brand, Device, Inventory
# Register your models here.

class DeviceCategroyAdminView(admin.ModelAdmin):
    list_display = ('id', 'category')

class BrandAdminView(admin.ModelAdmin):
    list_display = ('id','brand')

class DeviceAdminView(admin.ModelAdmin):
    list_display = ('id','category','brand','model','price','screen_size','storage_capacity','storage_type','ram','os','battery','processor','camera','bluetooth','wifi','noise_cancelling','microphone','megapixel','sensor','lens','zoom','video_resulation','gpu','cpu','ports','water_resistance','graphics_card','resolution','refresh_rate','created_at')


class InventoryAdminView(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'last_updated', 'created_at')




admin.site.register(DeviceCategories, DeviceCategroyAdminView)
admin.site.register(Brand, BrandAdminView)
admin.site.register(Device,DeviceAdminView)
admin.site.register(Inventory, InventoryAdminView)
