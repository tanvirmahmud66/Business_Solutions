# Generated by Django 4.2.10 on 2024-02-28 12:22

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_product_cost_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productImg',
            field=models.ImageField(blank=True, default='default_product_image.png', null=True, upload_to=app.models.product_image_path),
        ),
    ]