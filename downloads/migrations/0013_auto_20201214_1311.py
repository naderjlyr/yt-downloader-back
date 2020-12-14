# Generated by Django 3.0.8 on 2020-12-14 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('downloads', '0012_auto_20201209_0210'),
    ]

    operations = [
        migrations.RenameField(
            model_name='adult',
            old_name='genres',
            new_name='tags',
        ),
        migrations.AddField(
            model_name='adult',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='adult',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
