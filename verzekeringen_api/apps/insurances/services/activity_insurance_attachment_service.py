import logging, os

from django.core.files.base import File
from django.core.files.storage import default_storage

from apps.insurances.models import ActivityInsuranceAttachment
from apps.insurances.utils import InsuranceAttachmentUtils
from scouts_auth.inuits.files import StorageService
from scouts_auth.inuits.models import PersistedFile

logger = logging.getLogger(__name__)


class ActivityInsuranceAttachmentService:

    file_service: StorageService = default_storage

    def store_attachment(
        self, *, uploaded_file: File, insurance: ActivityInsuranceAttachment
    ) -> ActivityInsuranceAttachment:
        """Stores the uploaded attachment as a file."""

        name, extension = os.path.splitext(uploaded_file.name)
        file_name = InsuranceAttachmentUtils.generate_participant_list_file_name(insurance, extension)
        logger.debug("Storing attachment for insurance(%d) to %s", insurance.id, file_name)

        attachment = ActivityInsuranceAttachment()
        file = PersistedFile()
        file.file.save(name=file_name, content=uploaded_file)
        file.content_type = uploaded_file.content_type
        try:
            file.full_clean()
            file.save()
            attachment.insurance = insurance
            attachment.file = file
            attachment.full_clean()
            attachment.save()
        except Exception as exc:
            logger.error("An error occurred while persisting the attachment for insurance(%d)", insurance.id, exc)

        return attachment
