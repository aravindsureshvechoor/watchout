# Generated by Django 4.2.2 on 2023-09-12 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
