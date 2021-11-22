import logging
from datetime import datetime, date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction

from apps.insurances.models import InsuranceClaim, InsuranceClaimVictim
from apps.insurances.services import (
    InsuranceClaimReportService,
    InsuranceClaimAttachmentService,
    InsuranceClaimMailService,
)


logger = logging.getLogger(__name__)


class InsuranceClaimService:

    report_service = InsuranceClaimReportService()
    attachment_service = InsuranceClaimAttachmentService()
    mail_service = InsuranceClaimMailService()

    @transaction.atomic
    def create(
        self,
        *,
        created_by: settings.AUTH_USER_MODEL,
        declarant_city: str = None,
        group_group_admin_id: str,
        bank_account: str = None,
        date_of_accident: datetime,
        activity: str = None,
        activity_type: str = None,
        location: str = None,
        used_transport: str = None,
        damage_type: str = None,
        description: str = None,
        involved_party_description: str = None,
        involved_party_name: str = None,
        involved_party_birthdate: date = None,
        official_report_description: str = None,
        pv_number: str = None,
        witness_name: str = None,
        witness_description: str = None,
        leadership_description: str = None,
        victim: InsuranceClaimVictim,
        file=None,
    ) -> InsuranceClaim:
        # validate if person have rights to create claim for this group
        if group_group_admin_id not in (group.group_admin_id for group in created_by.scouts_groups):
            raise ValidationError("Given group %s is not a valid group of user" % group_group_admin_id)

        # Assuming that the group_admin_id has been loaded when adding the victim to the claim
        # @ricardo: check this please
        # if victim.group_admin_id:
        #     victim.get_member_number()
        victim.save()

        claim = InsuranceClaim(
            date=datetime.now(),
            declarant=created_by,
            declarant_city=declarant_city,
            group_group_admin_id=group_group_admin_id,
            bank_account=bank_account,
            date_of_accident=date_of_accident,
            activity=activity,
            activity_type=activity_type,
            location=location,
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
        )

        claim.full_clean()
        claim.save()

        if file.get("file", None):
            self.attachment_service.store_attachment(uploaded_file=file.get("file"), claim=claim)

        return claim

    def claim_update(*, claim: InsuranceClaim, **fields) -> InsuranceClaim:
        claim.note = fields.get("note", claim.note)
        claim.case_number = fields.get("case_number", claim.case_number)

        claim.full_clean()
        claim.save()

        return claim

    def email_claim(self, claim: InsuranceClaim):
        logger.debug("Generating pdf for claim(%d) and emailing the claim report", claim.id)
        claim_report_path = self.report_service.generate_pdf(claim)

        self.mail_service.send_claim(claim=claim, claim_report_path=claim_report_path)
