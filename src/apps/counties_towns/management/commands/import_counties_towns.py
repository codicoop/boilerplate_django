import json

from django.core.management.base import BaseCommand

from apps.counties_towns.models import County, Town


class Command(BaseCommand):
    help = "Imports Counties"
    with open("apps/counties_towns/fixtures/counties.json", 'r') as c:
        counties_source = json.load(c)
    with open("apps/counties_towns/fixtures/towns.json", 'r') as t:
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
            print(f"Creada comarca: {obj.name}")

    def import_towns(self):
        Town.objects.all().delete()
        for town in self.towns_source:
            name = town["nom"]
            if self.get_hardcoded_town(town["nom"]):
                name = self.get_hardcoded_town(town["nom"])
                print(f"Name of {town['nom']} resolved to {name}")
            obj = Town.objects.create(
                name=name,
                name_for_justification=name,
                county_id=int(town["codi_comarca"]),
            )
            print(f"Creada població: {obj.name}")

    def get_hardcoded_town(self, name):
        equivalencies = {
            "Brunyola i Sant Martí Sapresa": "BRUNYOLA",
            "Calonge i Sant Antoni": "CALONGE",
            "Bigues i Riells del Fai": "BIGUES I RIELLS",
            "Ràpita, la": "SANT CARLES DE LA RAPITA",
            "Roda de Berà": "RODA DE BARA",
            "Saus, Camallera i Llampaies": "SAUS,CAMALLERA I LLAMPAIES",
        }
        return equivalencies.get(name)
