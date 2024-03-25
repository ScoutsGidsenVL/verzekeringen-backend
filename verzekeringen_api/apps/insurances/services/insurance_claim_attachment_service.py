import logging
import os

from django.core.files.base import File
from django.core.files.storage import default_storage

from apps.insurances.models import InsuranceClaimAttachment
from apps.insurances.utils import InsuranceAttachmentUtils
from scouts_auth.inuits.files import StorageService
from scouts_auth.inuits.models import PersistedFile

logger = logging.getLogger(__name__)


class InsuranceClaimAttachmentService:
    file_service: StorageService = default_storage

    def store_attachment(self, *, uploaded_file: File, claim: InsuranceClaimAttachment) -> InsuranceClaimAttachment:
        """Stores the uploaded attachment as a file."""

        name, extension = os.path.splitext(uploaded_file.name)
        file_name = InsuranceAttachmentUtils.generate_claim_attachment_file_name(claim, extension)
        logger.debug("Storing attachment for claim(%d) to %s", claim.id, file_name)

        attachment = InsuranceClaimAttachment()
        file = PersistedFile()
        file.file.save(name=file_name, content=uploaded_file)
        file.content_type = uploaded_file.content_type

        try:
            file.full_clean()
            file.save()

            attachment = InsuranceClaimAttachment()
            attachment.insurance_claim = claim
            attachment.file = file

            attachment.full_clean()
            attachment.save()
        except Exception as exc:
            logger.error("An error occurred while persisting the attachment for claim (%d)", claim.id, exc)

        return attachment
