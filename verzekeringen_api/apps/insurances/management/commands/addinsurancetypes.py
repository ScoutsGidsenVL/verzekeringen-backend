from django.core.management.base import BaseCommand, CommandError
from ...models import InsuranceType


class Command(BaseCommand):

    help = "Adds the insurance types to the database"

    def handle(self, *args, **options):
        try:
            InsuranceType.objects.get(pk=1)
        except InsuranceType.DoesNotExist:
            type = InsuranceType(
                id=1, name="TypeEenmaligeActiviteit", description="Eenmalige activiteit", max_term="0"
            )
            type.save()
        try:
            InsuranceType.objects.get(pk=2)
        except InsuranceType.DoesNotExist:
            type = InsuranceType(
                id=2, name="TypeTijdelijkeVerzekering", description="Tijdelijke verzekering niet-leden", max_term="31"
            )
            type.save()
        try:
            InsuranceType.objects.get(pk=3)
        except InsuranceType.DoesNotExist:
            type = InsuranceType(
                id=3, name="TypeEthiasAssistanceZonderAuto", description="Reisbijstand, zonder auto", max_term="0"
            )
            type.save()
        try:
            InsuranceType.objects.get(pk=4)
        except InsuranceType.DoesNotExist:
            type = InsuranceType(
                id=4, name="TypeEthiasAssistanceMetAuto", description="Reisbijstand, met auto", max_term="0"
            )
            type.save()
        try:
            InsuranceType.objects.get(pk=5)
        except InsuranceType.DoesNotExist:
            type = InsuranceType(
                id=5, name="TypeTijdelijkeAutoverzekering", description="Autoverzekering", max_term="30"
            )
            type.save()
        try:
            InsuranceType.objects.get(pk=6)
        except InsuranceType.DoesNotExist:
            type = InsuranceType(
                id=6, name="TypeGroepsmateriaalVerzekering", description="Materiaal verzekering", max_term="30"
            )
            type.save()
        try:
            InsuranceType.objects.get(pk=10)
        except InsuranceType.DoesNotExist:
            type = InsuranceType(
                id=10, name="TypeEvenementenVerzekering", description="Evenementen verzekering", max_term="0"
            )
            type.save()
