# Generated by Django 3.0.1 on 2019-12-27 09:32

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='Email')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='Last name')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('classEnrolled', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('classUnderTaken', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None)),
            ],
        ),
    ]
