from django.core.validators import validate_image_file_extension
from django.db import models
from django.utils.translation import gettext_lazy as _
from sorl.thumbnail import ImageField

from project.storage_backends import PublicMediaStorage


class Data(models.Model):
    class RadioChoices(models.TextChoices):
        OPTION_1 = "OP1", _("Option 1")
        OPTION_2 = "OP2", _("Option 2")
        OPTION_3 = "OP3", _("Option 3")

    class SelectChoices(models.TextChoices):
        OPTION_1 = "OP1", _("Option 1")
        OPTION_2 = "OP2", _("Option 2")
        OPTION_3 = "OP3", _("Option 3")

    class SelectCheckboxChoices(models.TextChoices):
        OPTION_1 = "OP1", _("Option 1")
        OPTION_2 = "OP2", _("Option 2")
        OPTION_3 = "OP3", _("Option 3")

    field_text_1 = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        help_text="Help field_text_1",
    )
    field_text_2 = models.CharField(
        max_length=100,
        blank=True,
        null=False,
        help_text="Help field_text_2",
    )
    field_email = models.EmailField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        help_text="Help field_email",
    )
    field_radio = models.CharField(
        max_length=4,
        choices=RadioChoices.choices,
        default=RadioChoices.OPTION_1,
        blank=True,
        null=False,
        help_text="Help field_radio",
    )
    field_boolean_checkbox = models.BooleanField(
        default=False,
        blank=False,
        null=False,
        help_text="Help field_boolean_checkbox",
    )
    field_select_dropdown = models.CharField(
        max_length=4,
        choices=SelectChoices.choices,
        default=SelectChoices.OPTION_1,
        blank=False,
        null=False,
        help_text="Help field_select_dropdown",
    )
    field_password = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        help_text="Help field_password",
    )
    field_password_confirm = models.CharField(
        max_length=50,
        blank=True,
        null=False,
        help_text="Help field_password_confirm",
    )
    field_number = models.IntegerField(
        blank=True,
        default=0,
        help_text="Help field_number",
    )
    field_select_checkbox = models.CharField(
        max_length=250,
        default=SelectCheckboxChoices.OPTION_1,
        blank=True,
        help_text="Help field_select_checkbox",
    )
    field_image = ImageField(
        "Sorl thumbnail Image field",
        storage=PublicMediaStorage(),
        blank=True,
        default="",
        validators=[validate_image_file_extension],
    )
    field_file = models.FileField(
        "Generic file field",
        storage=PublicMediaStorage(),
        blank=True,
        default="",
    )
    field_time = models.TimeField(
        "Time field",
        blank=True,
        null=True,
        help_text="Help text for Time field.",
    )
    field_date = models.DateField(
        "Generic date field",
        blank=True,
        null=True,
        default=None,
        help_text="Help text for field_date",
    )

    def __str__(self):
        return f"{self.field_text_1}"
