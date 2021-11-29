import os, json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from scouts_insurances.locations.models import Country

from scouts_insurances.insurances.models import InsuranceType


class Command(BaseCommand):

    help = "Adds an initial list of countries to the database for each InsuranceType"

    def handle(self, *args, **options):
        parent_path = Path(settings.BASE_DIR)
        data_path = "scouts_insurances/management/initial_data/countries.json"
        all_countries_path = os.path.join(parent_path, data_path)

        # Clear insurance types for all countries
        countries: list[Country] = Country.objects.all()
        for country in countries:
            country.insurance_types.clear()

        # Load json file
        with open(all_countries_path, "r") as stream:
            content = stream.read()
            countries = json.loads(content)

        # assign insurance countries
        for country in countries:
            print(country["name"])
            obj: Country = Country.objects.filter(name=country["name"]).get_or_create(name=country["name"])[0]
            for type in country["applicable_types"]:
                print("\t - %s" % (type))
                obj.insurance_types.add(InsuranceType.objects.filter(name=type).get())

            obj.save()
