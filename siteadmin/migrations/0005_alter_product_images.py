# Generated by Django 4.2.2 on 2023-09-12 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteadmin', '0004_alter_product_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ImageField(upload_to=''),
        ),
    ]
