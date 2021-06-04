import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from apps.insurances.models import InsuranceType
from ...models import Country


class Command(BaseCommand):

    help = "Adds an initial list of countries to the database for each InsuranceType"

    def handle(self, *args, **options):
        all_countries_path = os.path.join(
            settings.BASE_DIR, "apps/locations/management/initial_data/all_countries.txt"
        )

        with open(all_countries_path, "r") as stream:
            all_country_names = stream.read().splitlines()

        for name in all_country_names:
            countries = Country.objects.filter(name=name)
            if not countries:
                country = Country(name=name)
                country.full_clean()
                country.save()
            else:
                country = countries[0]
            country.insurance_types.clear()
            country.insurance_types.add(InsuranceType.objects.temporary())
            country.insurance_types.add(InsuranceType.objects.travel_assistance_without_vehicle())
            country.insurance_types.add(InsuranceType.objects.travel_assistance_with_vehicle())
            country.insurance_types.add(InsuranceType.objects.temporary_vehicle())
            country.insurance_types.add(InsuranceType.objects.equipment())
            country.save()
