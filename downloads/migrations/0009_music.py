# Generated by Django 3.0.8 on 2020-12-08 16:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('downloads', '0008_auto_20201202_1905'),
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('artist', models.CharField(blank=True, max_length=100, null=True)),
                ('genre', models.CharField(blank=True, max_length=100, null=True)),
                ('duration', models.CharField(blank=True, max_length=40, null=True)),
                ('url', models.CharField(blank=True, max_length=300, null=True)),
                ('download_link', models.CharField(blank=True, max_length=300, null=True)),
                ('image', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
