import json

from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from apps.counties_towns.models import County, Town


class Command(BaseCommand):
    help = "Imports Counties"
    with open("apps/counties_towns/fixtures/counties.json", "r") as c:
        counties_source = json.load(c)
    with open("apps/counties_towns/fixtures/towns.json", "r") as t:
        towns_source = json.load(t)

    def handle(self, *args, **options):
        self.import_counties()
        self.import_towns()

    def import_counties(self):
        County.objects.all().delete()
        for county in self.counties_source:
            obj = County.objects.create(
                id=int(county["codi"]),
                name=county["nom"],
            )
            print(_("County created: %s") % obj.name)

    def import_towns(self):
        Town.objects.all().delete()
        for town in self.towns_source:
            obj = Town.objects.create(
                name=town["nom"],
                county_id=int(town["codi_comarca"]),
            )
            print(_("Creada població: %s") % obj.name)
