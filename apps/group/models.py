from django.db import models

from apps.group.querysets import TertiaryGroupQuerySet


class Regional(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class TertiaryGroup(models.Model):
    name = models.CharField(max_length=120)
    regional = models.ForeignKey(Regional, on_delete=models.PROTECT, related_name='tertiarygroups')

    objects = TertiaryGroupQuerySet.as_manager()

    def __str__(self):
        return self.name
