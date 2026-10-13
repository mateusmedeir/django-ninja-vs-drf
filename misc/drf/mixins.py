class UserScopedQuerysetMixin:
    """Narrows the view's queryset to what the requesting user may see."""

    def get_queryset(self):
        return super().get_queryset().visible_to(self.request.user)
