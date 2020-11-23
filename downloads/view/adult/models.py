from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.utils import timezone


class Adult(models.Model):
    name = models.CharField(max_length='200', null=True, blank=True)
    farsi_name = models.CharField(max_length='100', null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    movie_id = models.CharField(max_length=40, null=True, blank=True)
    genres = models.CharField(max_length=40, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    download_links = ArrayField(JSONField(null=True, blank=True), null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
