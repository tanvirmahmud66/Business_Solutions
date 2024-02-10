# Generated by Django 4.2.10 on 2024-02-09 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_devicecategories_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=255)),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('screen_size', models.CharField(blank=True, max_length=10, null=True)),
                ('storage_capacity', models.CharField(blank=True, max_length=255, null=True)),
                ('storage_type', models.CharField(blank=True, choices=[('SSD', 'SSD'), ('HDD', 'HDD')], max_length=255, null=True)),
                ('ram', models.CharField(blank=True, max_length=255, null=True)),
                ('os', models.CharField(blank=True, max_length=255, null=True)),
                ('battery', models.CharField(blank=True, max_length=255, null=True)),
                ('processor', models.CharField(blank=True, max_length=255, null=True)),
                ('camera', models.TextField(blank=True, null=True)),
                ('bluetooth', models.CharField(blank=True, max_length=255, null=True)),
                ('wifi', models.CharField(blank=True, max_length=255, null=True)),
                ('noise_cancelling', models.CharField(blank=True, choices=[('YES', 'YES'), ('NO', 'NO')], null=True)),
                ('microphone', models.CharField(blank=True, choices=[('YES', 'YES'), ('NO', 'NO')], null=True)),
                ('megapixel', models.CharField(blank=True, max_length=255, null=True)),
                ('sensor', models.CharField(blank=True, max_length=255, null=True)),
                ('lens', models.CharField(blank=True, max_length=255, null=True)),
                ('zoom', models.CharField(blank=True, max_length=255, null=True)),
                ('video_resulation', models.CharField(blank=True, max_length=255, null=True)),
                ('gpu', models.CharField(blank=True, max_length=255, null=True)),
                ('cpu', models.CharField(blank=True, max_length=255, null=True)),
                ('ports', models.CharField(blank=True, max_length=255, null=True)),
                ('water_resistance', models.CharField(blank=True, choices=[('YES', 'YES'), ('NO', 'NO')], null=True)),
                ('graphics_card', models.CharField(blank=True, max_length=255, null=True)),
                ('resolution', models.CharField(blank=True, max_length=255, null=True)),
                ('refresh_rate', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.devicecategories')),
            ],
        ),
        migrations.DeleteModel(
            name='Devices',
        ),
    ]
