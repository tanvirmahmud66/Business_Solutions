# Generated by Django 4.2.10 on 2024-03-21 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_productlineup_sale_confirm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='invoice_list',
        ),
        migrations.AddField(
            model_name='sales',
            name='amount',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='product_quantity',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
