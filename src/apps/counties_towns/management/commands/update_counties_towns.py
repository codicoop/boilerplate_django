import json
from urllib.request import urlopen

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _


class Command(BaseCommand):
    help = _("Update Catalan counties and towns")
    counties_source = json.loads(urlopen(settings.COUNTY_UPDATE_URL).read())
    towns_source = json.loads(urlopen(settings.TOWN_UPDATE_URL).read())

    def handle(self, *args, **options):
        with open("apps/counties_towns/fixtures/counties.json", "w") as c:
            json.dump(self.counties_source, c)
        with open("apps/counties_towns/fixtures/towns.json", "w") as t:
            json.dump(self.towns_source, t)
