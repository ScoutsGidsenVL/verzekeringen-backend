from decimal import Decimal
from django.core.management.base import BaseCommand

from apps.insurances.models import InsuranceType, CostVariable
from apps.insurances.models.enums import EventSize


class Command(BaseCommand):

    help = "Adds the cost variables to the database"

    def set_variable(self, type, key, value):
        try:
            cost_var = CostVariable.objects.get_variable(type, key)
        except CostVariable.DoesNotExist:
            cost_var = CostVariable(key=key, insurance_type=type)
        cost_var.value = value
        cost_var.full_clean()
        cost_var.save()

    def handle(self, *args, **options):
        # Activity
        type = InsuranceType.objects.activity()
        self.set_variable(type, "premium", Decimal(55))

        # Temporary
        type = InsuranceType.objects.temporary()
        self.set_variable(type, "premium", Decimal(4))

        # Travel Assistance without car
        type = InsuranceType.objects.travel_assistance_without_vehicle()
        areas = ("europe", "world")
        limits = (1, 3, 5, 11, 17, 23, 32, "extramonth")
        costs = {
            ("europe", 1): Decimal("2.14"),
            ("europe", 3): Decimal("4.21"),
            ("europe", 5): Decimal("7.6"),
            ("europe", 11): Decimal("11.15"),
            ("europe", 17): Decimal("14.75"),
            ("europe", 23): Decimal("18.36"),
            ("europe", 32): Decimal("22.13"),
            ("europe", "extramonth"): Decimal("11.15"),
            ("world", 1): Decimal("3.5"),
            ("world", 3): Decimal("6.89"),
            ("world", 5): Decimal("13.01"),
            ("world", 11): Decimal("18.52"),
            ("world", 17): Decimal("23.82"),
            ("world", 23): Decimal("31.74"),
            ("world", 32): Decimal("40.7"),
            ("world", "extramonth"): Decimal("18.52"),
        }
        for (area, limit), value in costs.items():
            self.set_variable(type, "premium_%s_%s" % (area, str(limit)), value)

        # Travel Assistance with car
        type = InsuranceType.objects.travel_assistance_with_vehicle()
        costs = {
            ("participant", 1): Decimal("2.14"),
            ("participant", 3): Decimal("4.21"),
            ("participant", 5): Decimal("7.6"),
            ("participant", 11): Decimal("11.15"),
            ("participant", 17): Decimal("14.75"),
            ("participant", 23): Decimal("18.36"),
            ("participant", 32): Decimal("22.13"),
            ("participant", "extramonth"): Decimal("11.15"),
            ("vehicle", 1): Decimal("6.22"),
            ("vehicle", 3): Decimal("12.25"),
            ("vehicle", 5): Decimal("22.06"),
            ("vehicle", 11): Decimal("32.49"),
            ("vehicle", 17): Decimal("42.90"),
            ("vehicle", 23): Decimal("53.50"),
            ("vehicle", 32): Decimal("64.44"),
            ("vehicle", "extramonth"): Decimal("32.49"),
        }
        for (option, limit), value in costs.items():
            self.set_variable(type, "premium_%s_%s" % (option, str(limit)), value)

        # Event insurance
        type = InsuranceType.objects.event()
        costs = {
            EventSize.FIVEHUNDRED: Decimal("65.55"),
            EventSize.THOUSAND: Decimal("131.10"),
            EventSize.THOUSANDFIVEHUNDRED: Decimal("163.88"),
            EventSize.TWOTHOUSAND: Decimal("229.43"),
            EventSize.TWOTHOUSANDFIVEHUNDRED: Decimal("0"),
        }
        for size, value in costs.items():
            self.set_variable(type, "premium_%s" % size, value)

        # Temporary vehicle insurance
        type = InsuranceType.objects.temporary_vehicle()

        costs = {
            ("option1", 8): Decimal("75.40"),
            ("option1", 15): Decimal("100.53"),
            ("option1", 25): Decimal("125.67"),
            ("option1", 31): Decimal("150.80"),
            ("option2A", 15): Decimal("32.99"),
            ("option2A", 31): Decimal("54.99"),
            ("option2B", 15): Decimal("42.89"),
            ("option2B", 31): Decimal("71.48"),
            ("option2C", 15): Decimal("46.18"),
            ("option2C", 31): Decimal("76.97"),
            ("option3", 15): Decimal("31.47"),
            ("option3", 20): Decimal("47.22"),
            ("option3", 31): Decimal("62.95"),
        }
        for (option, size), value in costs.items():
            self.set_variable(type, "premium_%s_%s" % (option, size), value)

        # Equipment insurance
        type = InsuranceType.objects.equipment()

        costs = {"minimum": Decimal("20.45"), "percentage": Decimal("0.00825")}

        for option, value in costs.items():
            self.set_variable(type, "premium_%s" % option, value)
