# Generated by Django 3.1 on 2020-09-04 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20200903_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='url_name',
            field=models.CharField(default='Laptop', max_length=200),
            preserve_default=False,
        ),
    ]