# Generated by Django 4.2.10 on 2024-02-13 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255)),
                ('price', models.PositiveIntegerField()),
                ('cost', models.PositiveBigIntegerField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.categories')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('contact_person', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('IN', 'IN'), ('OUT', 'OUT')], max_length=5)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Credit Card', 'Credit card'), ('Master Card', 'Master Card'), ('Bank Cheque', 'Bank cheque'), ('Bkash', 'Bkash'), ('Sure Cash', 'Sure Cash'), ('DBBL Mobile', 'DBBL Mobile'), ('DBBL Card', 'DBBL Card'), ('Nagad', 'Nagad'), ('UCash', 'UCash'), ('Payoneer', 'Payoneer')], max_length=50)),
                ('quantity', models.PositiveIntegerField()),
                ('amount', models.PositiveBigIntegerField()),
                ('transaction_code', models.CharField(max_length=255, unique=True)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('productId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
            ],
            options={
                'ordering': ['transaction_date'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='supplierId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.supplier'),
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
