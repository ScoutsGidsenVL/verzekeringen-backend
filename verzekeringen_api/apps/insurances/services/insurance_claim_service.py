import logging
from datetime import date, datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction

from apps.insurances.models import InsuranceClaim
from apps.insurances.services import (
    InsuranceClaimAttachmentService,
    InsuranceClaimReportService,
    InuitsInsuranceMailService,
)
from apps.people.models import InuitsClaimVictim

logger = logging.getLogger(__name__)


class InsuranceClaimService:

    report_service = InsuranceClaimReportService()
    attachment_service = InsuranceClaimAttachmentService()
    mail_service = InuitsInsuranceMailService()

    @transaction.atomic
    def create(
        self,
        *,
        group_group_admin_id: str,
        created_by: settings.AUTH_USER_MODEL,
        date_of_accident: datetime = None,
        declarant_city: str = "",
        file=None,
        bank_account: str = "",
        activity: str = "",
        activity_type: str = "",
        used_transport: str = "",
        damage_type: str = "",
        description: str = "",
        involved_party_description: str = "",
        involved_party_name: str = "",
        involved_party_birthdate: date = None,
        official_report_description: str = "",
        pv_number: str = "",
        witness_name: str = "",
        witness_description: str = "",
        leadership_description: str = "",
        victim: InuitsClaimVictim,
        witness: bool = None,
        involved_party: bool = None,
        official_report: bool = None,
        leadership: bool = None,
    ) -> InsuranceClaim:
        # validate if person has rights to create claim for this group
        if group_group_admin_id not in (group.group_admin_id for group in created_by.scouts_groups):
            raise ValidationError("Given group %s is not a valid group of user" % group_group_admin_id)

        victim.save()

        claim = InsuranceClaim(
            declarant=created_by,
            declarant_city=declarant_city,
            group_group_admin_id=group_group_admin_id,
            bank_account=bank_account,
            date_of_accident=date_of_accident,
            activity=activity,
            activity_type=activity_type,
            used_transport=used_transport,
            damage_type=damage_type,
            description=description,
            involved_party_description=involved_party_description,
            involved_party_name=involved_party_name,
            involved_party_birthdate=involved_party_birthdate,
            official_report_description=official_report_description,
            pv_number=pv_number,
            witness_name=witness_name,
            witness_description=witness_description,
            leadership_description=leadership_description,
            victim=victim,
            witness=witness,
            involved_party=involved_party,
            official_report=official_report,
            leadership=leadership,
            attachment_name=file.get("file").name if file.get("file", None) else None,
        )

        claim.full_clean()
        claim.save()

        if file.get("file", None):
            self.attachment_service.store_attachment(uploaded_file=file.get("file"), claim=claim)

        return claim

    def claim_update(*, claim: InsuranceClaim, **fields) -> InsuranceClaim:
        logger.debug("Updating claim %s with case_number and note", claim.id)
        claim.note = fields.get("note", claim.note)
        claim.case_number = fields.get("case_number", claim.case_number)

        claim.full_clean()
        claim.save()

        return claim

    def email_claim(self, claim: InsuranceClaim):
        logger.debug("Generating pdf for claim(%d) and emailing the claim report", claim.id)
        claim_report_path = self.report_service.generate_pdf(claim)

        self.mail_service.send_claim(claim=claim, claim_report_path=claim_report_path)
