# Generated by Django 4.2.10 on 2024-02-27 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_purchase_transaction_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='transaction_type',
            field=models.CharField(blank=True, default='OUT', null=True),
        ),
    ]