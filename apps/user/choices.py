from django.db import models


class UserLevel(models.TextChoices):
    TERTIARYGROUP = 'tertiarygroup', 'Tertiary group'
    REGIONAL = 'regional', 'Regional'
