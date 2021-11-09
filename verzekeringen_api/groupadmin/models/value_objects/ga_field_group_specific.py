from typing import List

from groupadmin.models.value_objects import ScoutsValue


class ScoutsGroupSpecificField:

    group_admin_id: str
    schema: List[str]
    values: List[ScoutsValue]

    def __init__(self, group: str = None, schema: List[str] = None, values: List[ScoutsValue] = None):
        self.group = group
        self.schema = schema if schema else []
        self.values = values if values else []

    def __str__(self):
        return "group ({}), schema({}), values({})".format(
            self.group,
            ", ".join(schema_item for schema_item in self.schema),
            ", ".join(value for value in self.values),
        )
