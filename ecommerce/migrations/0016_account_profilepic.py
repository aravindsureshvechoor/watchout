# Generated by Django 4.2.2 on 2023-10-10 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0015_referalid'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profilepic',
            field=models.ImageField(default=1, upload_to='photos/profilepic'),
            preserve_default=False,
        ),
    ]
