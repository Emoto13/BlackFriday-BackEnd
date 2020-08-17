# Generated by Django 3.0.8 on 2020-08-16 12:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('original_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=4)),
                ('description', models.TextField(default='')),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('city', models.CharField(default='', max_length=150)),
                ('in_store', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImageCatalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product', to='products.Product')),
                ('product_image', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_image', to='products.ProductImage')),
            ],
            options={
                'ordering': ['created'],
                'unique_together': {('product', 'product_image')},
            },
        ),
    ]