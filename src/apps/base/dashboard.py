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
                    "django.contrib.*",
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

        links_children = []

        if context["request"].user.is_superuser:
            links_children.append(
                [
                    _("Admin activity registry"),
                    "admin/logentry/",
                ]
            )

        self.children.append(
            modules.LinkList(title=_("Links"), column=3, children=links_children)
        )

        # TODO: Check if this old code is still necessary and clean up
        # self.children.append(
        #     modules.ModelList(
        #         _("Correus enviats"),
        #         column=1,
        #         collapsible=False,
        #         models=("mailqueue.*",),
        #     )
        # )

        # append another link list module for "support".
        # self.children.append(modules.LinkList(
        #     _('Enllaços'),
        #     column=2,
        #     children=[
        #         {
        #             'title': _('Django Documentation'),
        #             'url': 'http://docs.djangoproject.com/',
        #             'external': True,
        #         },
        #         {
        #             'title': _('Grappelli Documentation'),
        #             'url': 'http://packages.python.org/django-grappelli/',
        #             'external': True,
        #         },
        #         {
        #             'title': _('Grappelli Google-Code'),
        #             'url': 'http://code.google.com/p/django-grappelli/',
        #             'external': True,
        #         },
        #     ]
        # ))

        # self.children.append(
        #     modules.ModelList(
        #         _("Logs"),
        #         column=1,
        #         collapsible=False,
        #         models=("django.contrib.admin.models.LogEntry",),
        #     )
        # )
