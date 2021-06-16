from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from ...models import InfoVariable


class Command(BaseCommand):

    help = "Adds the info variables to the database"

    def set_variable(self, key, value):
        try:
            info_var = InfoVariable.objects.get(pk=key)
        except InfoVariable.DoesNotExist:
            info_var = InfoVariable(key=key)
        info_var.value = value
        info_var.full_clean()
        info_var.save()

    def handle(self, *args, **options):
        self.set_variable("test", "<div>HELLO WORLD</div>")
