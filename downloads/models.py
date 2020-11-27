from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.utils import timezone

from downloads.choices import MoviesChoices


class Adult(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    farsi_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    movie_id = models.CharField(max_length=40, null=True, blank=True)
    genres = ArrayField(models.CharField(max_length=40, null=True, blank=True), null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    download_links = ArrayField(JSONField(null=True, blank=True), null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class Educational(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    farsi_name = models.CharField(max_length=2018, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    categories = ArrayField(models.CharField(max_length=40, null=True, blank=True), null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    download_links = ArrayField(JSONField(null=True, blank=True), null=True, blank=True)
    url_slug = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    main_language = models.CharField(max_length=20, null=True, blank=True)


class Movie(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    farsi_name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    movie_id = models.CharField(max_length=40, null=True, blank=True)
    genres = ArrayField(models.CharField(max_length=20), null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    download_links = ArrayField(JSONField(null=True, blank=True), null=True, blank=True)
    movie_type = models.CharField(max_length=2, choices=MoviesChoices.choices, default=MoviesChoices.MOVIE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    country = models.CharField(max_length=30, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    main_language = models.CharField(max_length=20, null=True, blank=True)
    subtitles = ArrayField(
        JSONField(null=True, blank=True), null=True, blank=True,
    )
    duration = models.CharField(max_length=30, null=True, blank=True)
    imdb_rate = models.CharField(max_length=10, null=True, blank=True)
