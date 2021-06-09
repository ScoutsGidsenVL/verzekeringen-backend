# from datetime import datetime
# from decimal import Decimal
# from django.conf import settings
# from django.core.exceptions import ValidationError
# from apps.members.models import InuitsNonMember, Member
# from ..models import Equipment, InuitsEquipment


# def inuits_equipment_create(
#     *,
#     nature: str,
#     description: str,
#     total_value: Decimal,
#     group_id: str,
#     created_by: settings.AUTH_USER_MODEL,
#     owner_non_member: InuitsNonMember,
#     owner_member: dict = None,
# ) -> InuitsEquipment:
#     # validate group
#     if group_id not in (group.id for group in created_by.partial_scouts_groups):
#         raise ValidationError("Given group %s is not a valid group of user" % group_id)
#     equipment = InuitsEquipment(
#         nature=nature,
#         description=description,
#         total_value=total_value,
#         group_number=group_id,
#     )
#     equipment.full_clean()
#     equipment.save()

#     return equipment
