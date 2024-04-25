"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from apps.demo.views import data_view, detail_view, list_view, update_view
from project.views import RootRedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RootRedirectView.as_view()),
]

urlpatterns += i18n_patterns(
    path("", data_view, name="home"),
    path("data/list/", list_view, name="list"),
    path(_("data/details/<int:id>"), detail_view, name="details"),
    path(_("data/update/<int:id>"), update_view, name="update"),
    path(_("registration/"), include("apps.users.urls", namespace="registration")),
)
