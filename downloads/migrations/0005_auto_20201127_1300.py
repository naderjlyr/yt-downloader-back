# Generated by Django 3.0.8 on 2020-11-27 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('downloads', '0004_auto_20201127_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='movie_type',
            field=models.CharField(choices=[('MV', 'movies'), ('SR', 'series')], default='MV', max_length=2),
        ),
    ]
