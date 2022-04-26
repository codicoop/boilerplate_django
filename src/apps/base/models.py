import uuid

from django.db import models
from django.utils.formats import localize
from django.utils.text import Truncator


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, null=False, editable=False)
    created_by = models.ForeignKey(
        "users.User",
        null=False,
        blank=False,
        related_name="%(app_label)s_%(class)s_related",
        on_delete=models.CASCADE,
        verbose_name="autor",
    )

    class Meta:
        abstract = True

    def __str__(self, field: str = None, str_len: int = 30):
        if field and hasattr(self, field):
            field = getattr(self, field)
            summary = Truncator(field).chars(str_len)
            return f"{summary} ({localize(self.created)})"
        return f"{self.id} ({localize(self.created)})"
