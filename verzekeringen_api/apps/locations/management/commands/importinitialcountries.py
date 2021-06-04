from django.core.management.base import BaseCommand, CommandError
from apps.insurance.models import InsuranceType
from ...models import Country


class Command(BaseCommand):

    help = "Adds an initial list of countries to the database for each InsuranceType"

    def handle(self, *args, **options):
        pass
