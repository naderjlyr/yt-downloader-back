# Generated by Django 3.0.8 on 2020-12-08 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('downloads', '0011_auto_20201209_0203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='artist',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='name',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]