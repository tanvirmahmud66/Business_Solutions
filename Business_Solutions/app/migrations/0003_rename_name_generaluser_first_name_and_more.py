# Generated by Django 4.2.10 on 2024-03-18 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_generaluser_productlineup_sales'),
    ]

    operations = [
        migrations.RenameField(
            model_name='generaluser',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='generaluser',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]