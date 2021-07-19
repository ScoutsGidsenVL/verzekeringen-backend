import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from apps.insurances.models import InsuranceType
from ...models import Country
import json


class Command(BaseCommand):

    help = "Adds an initial list of countries to the database for each InsuranceType"

    def handle(self, *args, **options):
        all_countries_path = os.path.join(
            settings.BASE_DIR, "apps/locations/management/initial_data/countries.json"
        )

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
            print(country['name'])
            obj: Country = Country.objects.filter(name=country['name']).get_or_create(name=country['name'])[0]
            for type in country['applicable_types']:
                print("\t - %s" % (type))
                obj.insurance_types.add(InsuranceType.objects.filter(name=type).get())

            obj.save()