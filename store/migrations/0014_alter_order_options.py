# Generated by Django 5.1.3 on 2024-11-22 03:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel order')]},
        ),
    ]
