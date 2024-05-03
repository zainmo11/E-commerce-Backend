# Generated by Django 5.0.4 on 2024-04-28 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='cart_item',
            new_name='product',
        ),
        migrations.AddConstraint(
            model_name='cartitem',
            constraint=models.UniqueConstraint(fields=('customer', 'product'), name='user_cart_item_constraint'),
        ),
    ]
