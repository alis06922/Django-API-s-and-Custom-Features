# Generated by Django 5.1.3 on 2024-11-12 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_address_zip_code'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['last_name', 'first_name'], name='store_cutom_last_na_723f5c_idx'),
        ),
        migrations.AlterModelTable(
            name='customer',
            table='store_cutomers',
        ),
    ]