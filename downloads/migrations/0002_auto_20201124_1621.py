# Generated by Django 3.0.8 on 2020-11-24 13:21

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('downloads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adult',
            name='genres',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=40, null=True), blank=True, null=True, size=None),
        ),
    ]
