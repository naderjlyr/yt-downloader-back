# Generated by Django 3.0.8 on 2020-12-02 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloads', '0006_adult_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='educational',
            old_name='url_slug',
            new_name='url',
        ),
    ]
