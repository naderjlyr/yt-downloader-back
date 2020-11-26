# Generated by Django 3.0.8 on 2020-11-24 13:53

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('downloads', '0002_auto_20201124_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='educational',
            name='url_slug',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='educational',
            name='categories',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=40, null=True), blank=True, null=True, size=None),
        ),
    ]
