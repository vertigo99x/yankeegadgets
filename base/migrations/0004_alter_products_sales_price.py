# Generated by Django 4.1.6 on 2023-09-10 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_products_brand_products_color_products_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='sales_price',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=8, null=True),
        ),
    ]
