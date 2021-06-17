import os
import yaml
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
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
        yaml_path = os.path.join(settings.BASE_DIR, "apps/info/management/initial_data/initial_info.yml")

        with open(yaml_path, "r") as stream:
            try:
                info_vars = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        for key, value in info_vars.items():
            self.set_variable(key, value)
