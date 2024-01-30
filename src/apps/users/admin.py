from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone

from apps.base.admin import ModelAdminMixin
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
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        "email",
        "full_name",
        "is_superuser",
        "created_at",
        "created_by",
        "updated_at",
    )
    list_filter = ("is_superuser",)
    fieldsets = (
        (None, {"fields": ("email", "name", "password")}),
        # ('Personal info', {'fields': ('date_of_birth',)}),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "is_active")}),
        ("Metadata", {"fields": (
            "created_by",
            "created_at",
            "updated_at",
        )}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2")}),
        ("Permissions", {"fields": ("is_superuser",)}),
    )
    search_fields = (
        "email",
        "name",
        "surname",
    )
    ordering = ("email",)
    # filter_horizontal = ()
    superuser_fields = ("is_superuser", "is_active", "is_staff")
