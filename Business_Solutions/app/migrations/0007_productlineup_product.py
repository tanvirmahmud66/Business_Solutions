# Generated by Django 4.2.10 on 2024-03-19 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_generaluser_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='productlineup',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.product'),
        ),
    ]
