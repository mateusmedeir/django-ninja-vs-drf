from django.db import models

from apps.user.choices import UserLevel


class TertiaryGroupQuerySet(models.QuerySet):
    def visible_to(self, user):
        if user.is_superuser:
            return self
        if user.level == UserLevel.REGIONAL:
            return self.filter(regional_id=user.regional_id)
        if user.level == UserLevel.TERTIARYGROUP:
            return self.filter(id=user.tertiarygroup_id)
        return self.none()
