import logging

from django.core.files.base import File

from apps.insurances.models import InsuranceClaimAttachment


logger = logging.getLogger(__name__)


class InsuranceClaimAttachmentService:
    def store_attachment(self, *, uploaded_file: File, claim: InsuranceClaimAttachment) -> InsuranceClaimAttachment:
        logger.debug("Storing attachment for claim with id %s", claim.id)
        
        attachment = InsuranceClaimAttachment()
        attachment.insurance_claim = claim
        attachment.file.save(name=uploaded_file.name, content=uploaded_file)
        attachment.content_type = uploaded_file.content_type
        attachment.full_clean()
        attachment.save()

        return attachment
