# Generated by Django 5.0 on 2023-12-30 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_productcategory_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_short_desc',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
