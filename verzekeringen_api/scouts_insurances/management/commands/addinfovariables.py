import logging, os, yaml
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from scouts_insurances.info.models import InfoVariable


logger = logging.getLogger(__name__)


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
        parent_path = Path(settings.BASE_DIR)
        data_path = "scouts_insurances/management/initial_data/initial_info.yml"
        yaml_path = os.path.join(parent_path, data_path)

        logger.debug("Loading info variables from %s/%s", parent_path, data_path)

        with open(yaml_path, "r") as stream:
            try:
                info_vars = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        for key, value in info_vars.items():
            self.set_variable(key, value)
