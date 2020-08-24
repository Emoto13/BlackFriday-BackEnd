# Generated by Django 3.1 on 2020-08-22 14:55

import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('address', models.TextField(default='')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=150)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('account_title', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=30, max_digits=50, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=30, max_digits=50, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'), ('Prefer not to specify', 'Prefer not to specify')], max_length=50)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
