# Generated by Django 3.1 on 2020-09-09 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='products',
            new_name='product',
        ),
    ]