from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class Educational(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    farsi_name = models.CharField(max_length1=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    categories = models.CharField(max_length=40, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    download_links = ArrayField(JSONField(null=True, blank=True), null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    main_language = models.CharField(max_length=20, null=True, blank=True)
