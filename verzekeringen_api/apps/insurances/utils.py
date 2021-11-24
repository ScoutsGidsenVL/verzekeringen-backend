import logging

from django.conf import settings
from django.core.exceptions import ValidationError

from apps.insurances.models import InsuranceClaim, BaseInsurance

from inuits.utils import GlobalSettingsUtil


logger = logging.getLogger(__name__)


class InsuranceSettingsHelper:
    @staticmethod
    def is_test() -> bool:
        return getattr(settings, "DEBUG", False) and GlobalSettingsUtil.instance().is_test

    @staticmethod
    def get_email_insurance_from():
        return getattr(settings, "EMAIL_INSURANCE_FROM")

    @staticmethod
    def get_insurer_address() -> str:
        if InsuranceSettingsHelper.is_test():
            address = getattr(settings, "EMAIL_INSURER_ADDRESS_DEBUG", None)
            if not address:
                raise ValidationError("EMAIL_ADDRESS_INSURER_DEBUG is not set !")

            return address
        return getattr(settings, "EMAIL_INSURER_ADDRESS")

    @staticmethod
    def get_victim_email(victim_email: str = None) -> str:
        if InsuranceSettingsHelper.is_test():
            address = getattr(settings, "EMAIL_VICTIM_ADDRESS_DEBUG", None)
            if not address:
                raise ValidationError("EMAIL_VICTIM_ADDRESS_DEBUG is not set !")
            return address
        if not victim_email:
            raise ValidationError("Victim email is not set !")
        return victim_email

    @staticmethod
    def get_declarant_email(declarant_email: str = None) -> str:
        if InsuranceSettingsHelper.is_test():
            address = getattr(settings, "EMAIL_DECLARANT_ADDRESS_DEBUG", None)
            if not address:
                raise ValidationError("EMAIL_DECLARANT_ADDRESS_DEBUG is not set !")
            return address
        if not declarant_email:
            raise ValidationError("Declarant email not set")
        return declarant_email


class InsuranceAttachmentUtils:

    static_setup = False

    insurance_base_path = settings.INSURANCE_FILES_BASE_PATH
    insurance_prefix = settings.INSURANCE_CLAIM_FILE_NAME_PREFIX

    claim_base_path = settings.INSURANCE_CLAIM_FILES_BASE_PATH
    claim_prefix = settings.INSURANCE_CLAIM_FILE_NAME_PREFIX
    claim_suffix = settings.INSURANCE_CLAIM_FILE_NAME_SUFFIX

    @staticmethod
    def get_insurance_base_path() -> str:
        InsuranceAttachmentUtils._static_setup()

        return InsuranceAttachmentUtils.insurance_base_path

    @staticmethod
    def get_insurance_prefix() -> str:
        InsuranceAttachmentUtils._static_setup()

        return InsuranceAttachmentUtils.insurance_prefix

    @staticmethod
    def get_claim_base_path() -> str:
        InsuranceAttachmentUtils._static_setup()

        return InsuranceAttachmentUtils.claim_base_path

    @staticmethod
    def get_claim_prefix() -> str:
        InsuranceAttachmentUtils._static_setup()

        return InsuranceAttachmentUtils.claim_prefix

    @staticmethod
    def get_claim_suffix() -> str:
        InsuranceAttachmentUtils._static_setup()

        return InsuranceAttachmentUtils.claim_suffix

    @staticmethod
    def _clean(input: str, search: str, replace: str):
        return input.replace(search, replace)

    @staticmethod
    def _static_setup():
        if not InsuranceAttachmentUtils.static_setup:
            if InsuranceAttachmentUtils.insurance_base_path[-1] != "/":
                logger.warn("INSURANCES_FILES_BASE_PATH should end with a slash")
                InsuranceAttachmentUtils.insurance_base_path = InsuranceAttachmentUtils.insurance_base_path + "/"
            if InsuranceAttachmentUtils.claim_base_path[-1] != "/":
                logger.warn("INSURANCE_CLAIM_FILES_BASE_PATH should end with a slash")
                InsuranceAttachmentUtils.claim_base_path = InsuranceAttachmentUtils.claim_base_path + "/"

            InsuranceAttachmentUtils.insurance_prefix = InsuranceAttachmentUtils._clean(
                InsuranceAttachmentUtils.insurance_prefix, " ", "_"
            )
            InsuranceAttachmentUtils.claim_prefix = InsuranceAttachmentUtils._clean(
                InsuranceAttachmentUtils.claim_prefix, " ", "_"
            )
            InsuranceAttachmentUtils.claim_suffix = InsuranceAttachmentUtils._clean(
                InsuranceAttachmentUtils.claim_suffix, " ", "_"
            )

    @staticmethod
    def generate_temp_file_name(id, prefix: str, suffix: str) -> str:
        InsuranceAttachmentUtils._static_setup()

        return "%s_%010d%s" % (prefix, id, suffix)

    @staticmethod
    def generate_report_name(id, base_path: str, prefix: str, extension: str) -> str:
        InsuranceAttachmentUtils._static_setup()
        return "%s%s_%010d%s" % (
            base_path,
            prefix,
            id,
            ".pdf",
        )

    @staticmethod
    def generate_attachment_file_name(id, base_path: str, prefix: str, extension: str, suffix: str = None) -> str:
        InsuranceAttachmentUtils._static_setup()

        if suffix:
            return "%s%s_%010d_%s%s" % (
                base_path,
                prefix,
                id,
                suffix,
                extension,
            )

        return "%s%s_%010d%s" % (
            base_path,
            prefix,
            id,
            extension,
        )

    @staticmethod
    def generate_temp_file_name(id, prefix: str, suffix: str) -> str:
        InsuranceAttachmentUtils._static_setup()

        return "%s_%010d%s" % (prefix, id, suffix)

    @staticmethod
    def generate_claim_report_temp_file_name(claim: InsuranceClaim) -> str:
        return InsuranceAttachmentUtils.generate_temp_file_name(
            claim.id, InsuranceAttachmentUtils.insurance_prefix, ".pdf"
        )

    @staticmethod
    def generate_claim_report_file_name(claim: InsuranceClaim) -> str:
        return InsuranceAttachmentUtils.generate_report_name(
            claim.id,
            InsuranceAttachmentUtils.insurance_base_path,
            InsuranceAttachmentUtils.insurance_prefix,
            ".pdf",
        )

    @staticmethod
    def generate_claim_attachment_file_name(claim: InsuranceClaim, extension: str) -> str:
        return InsuranceAttachmentUtils.generate_attachment_file_name(
            claim.id,
            InsuranceAttachmentUtils.claim_base_path,
            InsuranceAttachmentUtils.claim_prefix,
            extension,
            InsuranceAttachmentUtils.claim_suffix,
        )

    @staticmethod
    def generate_insurance_attachment_file_name(insurance: BaseInsurance, extension: str) -> str:
        return InsuranceAttachmentUtils.generate_attachment_file_name(
            insurance.id,
            InsuranceAttachmentUtils.insurance_base_path,
            InsuranceAttachmentUtils.insurance_prefix,
            extension,
        )
