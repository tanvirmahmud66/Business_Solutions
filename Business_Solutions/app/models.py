from django.db import models

# Create your models here.

# ------------------------------------------------ Device Categories Model
class DeviceCategories(models.Model):
    category = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.category
    




# ------------------------------------------------ Brand Model 
class Brand(models.Model):
    brand = models.CharField(max_length=255)

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.brand
    




# ------------------------------------------------ Devices Model
class Device(models.Model):
    STORAGE_TYPE_CHOICES = [
        ('SSD', 'SSD'),
        ('HDD', 'HDD')
    ]
    BOOL_TYPE_CHOICES = [
        ('YES', 'YES'),
        ('NO','NO')
    ]
    category = models.ForeignKey(DeviceCategories, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    screen_size = models.CharField(max_length=10, null=True, blank=True)
    storage_capacity = models.CharField(max_length=255,null=True, blank=True)
    storage_type = models.CharField(max_length=255,null=True, blank=True, choices=STORAGE_TYPE_CHOICES)
    ram = models.CharField(max_length=255,null=True, blank=True)
    os = models.CharField(max_length=255, null=True, blank=True)
    battery = models.CharField(max_length=255,null=True, blank=True)
    processor = models.CharField(max_length=255, null=True, blank=True)
    camera = models.TextField(null=True, blank=True)
    bluetooth = models.CharField(max_length=255,null=True, blank=True)
    wifi = models.CharField(max_length=255, null=True, blank=True)
    noise_cancelling = models.CharField(null=True, blank=True, choices=BOOL_TYPE_CHOICES)
    microphone = models.CharField(null=True, blank=True, choices=BOOL_TYPE_CHOICES)
    megapixel = models.CharField(max_length=255,null=True, blank=True)
    sensor = models.CharField(max_length=255,null=True, blank=True)
    lens = models.CharField(max_length=255,null=True, blank=True)    
    zoom = models.CharField(max_length=255,null=True, blank=True)
    video_resulation = models.CharField(max_length=255,null=True, blank=True)
    gpu = models.CharField(max_length=255,null=True, blank=True)
    cpu = models.CharField(max_length=255,null=True, blank=True)
    ports = models.CharField(max_length=255,null=True, blank=True)
    water_resistance = models.CharField(null=True, blank=True, choices=BOOL_TYPE_CHOICES)
    graphics_card = models.CharField(max_length=255,null=True, blank=True)
    resolution = models.CharField(max_length=255,null=True, blank=True)
    refresh_rate = models.CharField(max_length=255,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model
    




# -------------------------------------------------- Inventory Model
class Inventory(models.Model):
    product = models.ForeignKey(Device, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.model




