"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.
To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'srv.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import gettext_lazy as _
from grappelli.dashboard import Dashboard, modules


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        # site_name = get_admin_site_name(context)

        self.children.append(
            modules.ModelList(
                _("Post Office"),
                column=1,
                collapsible=False,
                models=(
                    "post_office.models.Email",
                    "post_office.models.Log",
                    "post_office.models.EmailTemplate",
                    "post_office.models.Attachment",
                ),
            )
        )

        self.children.append(
            modules.ModelList(
                _("Accounts and authorization"),
                column=1,
                collapsible=False,
                models=(
                    "apps.users.models.User",
                    "django.contrib.*",  # It includes the logentry package
                ),
            )
        )

        self.children.append(
            modules.ModelList(
                _("Application parameters"),
                column=1,
                collapsible=False,
                models=("constance.*",),
            )
        )

        # append a recent actions module
        self.children.append(
            modules.RecentActions(
                _("Recent actions"),
                limit=5,
                collapsible=False,
                column=3,
            )
        )
