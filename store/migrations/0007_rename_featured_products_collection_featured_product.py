# Generated by Django 5.1.3 on 2024-11-13 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_rename_store_cutom_last_na_723f5c_idx_store_custo_last_na_2e448d_idx_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection',
            old_name='featured_products',
            new_name='featured_product',
        ),
    ]
