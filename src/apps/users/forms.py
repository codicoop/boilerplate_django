from constance import config
from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.utils import formats, timezone
from django.utils.translation import gettext_lazy as _

from project.helpers import absolute_url
from project.post_office import send
from apps.users.models import User
from project.widgets.checkbox import CheckboxInput
from project.fields.choicefield import ChoiceField


class AuthenticationForm(BaseAuthenticationForm):
    remember_me = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(), label=_("Remember me")
    )


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users with a different approach to password changing.
    """

    new_password = forms.CharField(
        label=_("Change password"),
        help_text=_(
            "The current password is not displayed for security reasons. "
            "Use this field and save the changes to set a new password. "
            "While writing the new password will be visible to make it easier "
            "for you to copy and send it to the user."
        ),
        max_length=150,
        required=False,
    )

    class Meta:
        model = User
        fields = ("email", "password", "is_active", "is_superuser")

    def save(self, commit=True):
        instance = super().save(commit)
        if self.cleaned_data.get("new_password", ""):
            instance.set_password(self.cleaned_data["new_password"])
        return instance


class UserSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "name",
            "surnames",
            "password1",
            "password2",
            "email",
        )

    accept_conditions = forms.BooleanField(
        label=_("I accept the data privacy policy"), required=True
    )
    test = forms.BooleanField(label="prova", widget=CheckboxInput())
    test_select = ChoiceField(label="Prova select")

    def save(self, commit=True):
        obj = super().save(commit)
        obj.set_boolean_datetime(
            "privacy_policy_accepted", self.cleaned_data["accept_conditions"]
        )
        return obj


class ProfileDetailsForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "name",
            "surnames",
            "email",
        )


class PasswordResetForm(BasePasswordResetForm):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        password_reset_url = absolute_url(
            reverse(
                "registration:password_reset_confirm",
                kwargs={
                    "uidb64": context["uid"],
                    "token": context["token"],
                },
            )
        )
        context = {
            "project_name": config.PROJECT_NAME,
            "user_name": context["user"].full_name,
            "date": str(
                formats.date_format(
                    timezone.now().date(),
                    format="SHORT_DATE_FORMAT",
                    use_l10n=True,
                )
            ),
            "time": str(formats.time_format(timezone.localtime(timezone.now()).time())),
            "user_email": context["email"],
            "absolute_url": settings.ABSOLUTE_URL,
            "password_reset_url": password_reset_url,
        }
        send(
            recipients=[
                to_email,
            ],
            template="password_reset",
            context=context,
        )
