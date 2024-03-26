from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from django.utils.html import format_html

from project.admin import ModelAdminMixin
from apps.users.forms import UserChangeForm
from apps.users.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.validated = timezone.now()
        if commit:
            user.save()
        return user


@admin.register(User)
class UserAdmin(ModelAdminMixin, BaseUserAdmin):
    list_display = (
        "email",
        "full_name",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("is_superuser",)
    search_fields = (
        "email",
        "name",
        "surnames",
    )
    ordering = ("email",)
    fieldsets = (("Autenticació", {"fields": ("email", "password")}),)
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            "Autenticació",
            {"classes": ("wide",), "fields": ("email", "password1", "password2")},
        ),
    )
    # common_fieldsets is not a standard ModelAdmin attribute. We extend
    # get_fieldsets to avoid having to repeat info in fieldsets and add_fieldsets.
    common_fieldsets = (
        (
            "Dades",
            {
                "fields": (
                    "name",
                    "surnames",
                )
            },
        ),
        (
            "Permisos i autoritzacions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "roles_explanation_field",
                    "groups",
                ),
            },
        ),
        (
            "Registre",
            {
                "fields": (
                    "created_by",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    superuser_fields = (
        "is_superuser",
    )
    readonly_fields = (
        "roles_explanation_field",
    )

    def get_fieldsets(self, request, obj=None):
        return super().get_fieldsets(request, obj) + self.common_fieldsets

    @admin.display(description="Informació rols d'usuari")
    def roles_explanation_field(self, obj):
        return format_html(
            """
            <ul>
              <li>Admins: accés a la configuració i personalització del
                backoffice, al llistat d'emails enviats pel sistema i a les
                plantilles de les notificacions. També pot editar els camps
                "Is staff" i "Is active" de la fitxa d'usuaris.
              </li>
            </ul>
            """
        )
