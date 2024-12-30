# Generated by Django 4.2.11 on 2024-11-11 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0032_alter_productattribute_product_class'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattribute',
            name='variants',
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='product_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='catalogue.productclass', verbose_name='Product type'),
        ),
    ]