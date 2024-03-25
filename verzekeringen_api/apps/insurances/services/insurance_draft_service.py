from django.conf import settings
from django.db import transaction

from apps.insurances.models import InsuranceDraft
from scouts_insurances.insurances.models import InsuranceType


class InsuranceDraftService:
    @transaction.atomic
    def insurance_draft_create(
        self, *, created_by: settings.AUTH_USER_MODEL, insurance_type: InsuranceType, data: dict, id: int = None
    ) -> InsuranceDraft:
        draft = InsuranceDraft(id=id, insurance_type=insurance_type, data=data, created_by=created_by)

        draft.full_clean()
        draft.save()

        return draft

    @transaction.atomic
    def insurance_draft_delete(self, *, draft: InsuranceDraft):
        draft.delete()

    @transaction.atomic
    def insurance_draft_update(self, *, draft: InsuranceDraft, **fields) -> InsuranceDraft:
        # For this update we just delete the old one and create a new one with the given fields (but same id)
        # Bit of a cheat but it matches expectations of customer
        old_id = draft.id
        self.insurance_draft_delete(draft=draft)
        new_draft = self.insurance_draft_create(**fields, id=old_id)
        return new_draft
