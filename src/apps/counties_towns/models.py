from django.db import models
from django.utils.translation import gettext_lazy as _


class County(models.Model):
    name = models.CharField(_("name"), max_length=50)

    class Meta:
        verbose_name = _("county")
        verbose_name_plural = _("counties")
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name


class Town(models.Model):
    county = models.ForeignKey(
        County,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )
    name = models.CharField(_("name"), max_length=250)

    class Meta:
        verbose_name = _("town")
        verbose_name_plural = _("towns")
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name
