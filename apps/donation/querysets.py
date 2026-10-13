from django.db import models

from apps.group.models import TertiaryGroup


class DonationQuerySet(models.QuerySet):
    def visible_to(self, user):
        return self.filter(tertiarygroup__in=TertiaryGroup.objects.visible_to(user))
