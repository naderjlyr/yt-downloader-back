from django.db import models
from django.utils.translation import ugettext_lazy as _


class MoviesChoices(models.TextChoices):
    MOVIE = "MV", _("movies")
    SERIES = "SR", _("series")
