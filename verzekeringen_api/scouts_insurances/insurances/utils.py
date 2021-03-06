import logging

from django.conf import settings
from django.core.exceptions import ValidationError

from apps.insurances.models import InsuranceClaim

from scouts_insurances.insurances.models import BaseInsurance

from scouts_auth.inuits.utils import GlobalSettingsUtil


logger = logging.getLogger(__name__)


class InsuranceSettingsHelper:
    @staticmethod
    def is_test() -> bool:
        return getattr(settings, "DEBUG", False) and GlobalSettingsUtil.instance().is_test

    @staticmethod
    def is_acceptance() -> bool:
        return InsuranceSettingsHelper.is_test() and getattr(settings, "IS_ACCEPTANCE", False)

    @staticmethod
    def get_email_insurance_from():
        return getattr(settings, "EMAIL_INSURANCE_FROM")

    @staticmethod
    def get_insurance_requester_address(insurance_requester_address: str = None, send_to: str = None) -> str:
        if InsuranceSettingsHelper.is_test():
            # When on acceptance, send everything to the requester
            if InsuranceSettingsHelper.is_acceptance():
                if not send_to:
                    raise ValidationError("Insurance requester email is not set")
                return send_to
            address = getattr(settings, "EMAIL_INSURANCE_REQUESTER_ADDRESS_DEBUG", None)
            if not address:
                raise ValidationError("EMAIL_INSURANCE_REQUESTER_ADDRESS_DEBUG is not set !")

            return address
        if not insurance_requester_address:
            raise ValidationError("Insurance requester address is not set !")

        return insurance_requester_address

    @staticmethod
    def get_insurer_address(insurer_address: str = None, send_to: str = None) -> str:
        if InsuranceSettingsHelper.is_test():
            # When on acceptance, send everything to the declarant
            if InsuranceSettingsHelper.is_acceptance():
                if not send_to:
                    raise ValidationError("Declarant email is not set")
                return send_to
            address = getattr(settings, "EMAIL_INSURER_ADDRESS_DEBUG", None)
            if not address:
                raise ValidationError("EMAIL_INSURER_ADDRESS_DEBUG is not set !")

            return address
        if not insurer_address:
            insurer_address = getattr(settings, "EMAIL_INSURER_ADDRESS", None)

        if not insurer_address:
            raise ValidationError("Insurer address is not set !")

        return None

    @staticmethod
    def get_company_identifier() -> str:
        return getattr(settings, "COMPANY_NON_MEMBER_DEFAULT_FIRST_NAME")


class InsuranceAttachmentUtils:

    static_setup = False

    insurance_base_path = settings.INSURANCE_FILES_BASE_PATH
    insurance_prefix = settings.INSURANCE_CLAIM_FILE_NAME_PREFIX

    @staticmethod
    def get_insurance_base_path() -> str:
        InsuranceAttachmentUtils._static_setup()

        return InsuranceAttachmentUtils.insurance_base_path

    @staticmethod
    def get_insurance_prefix() -> str:
        InsuranceAttachmentUtils._static_setup()

        return InsuranceAttachmentUtils.insurance_prefix

    @staticmethod
    def _clean(input: str, search: str, replace: str):
        return input.replace(search, replace)

    @staticmethod
    def _static_setup():
        if not InsuranceAttachmentUtils.static_setup:
            if InsuranceAttachmentUtils.insurance_base_path[-1] != "/":
                logger.warn("INSURANCES_FILES_BASE_PATH should end with a slash")
                InsuranceAttachmentUtils.insurance_base_path = InsuranceAttachmentUtils.insurance_base_path + "/"

            InsuranceAttachmentUtils.insurance_prefix = InsuranceAttachmentUtils._clean(
                InsuranceAttachmentUtils.insurance_prefix, " ", "_"
            )

    @staticmethod
    def generate_temp_file_name(id, prefix: str, suffix: str) -> str:
        return "%s_%010d%s" % (prefix, id, suffix)

    @staticmethod
    def generate_report_name(id, base_path: str, prefix: str, extension: str) -> str:
        return "%s%s_%010d%s" % (
            base_path,
            prefix,
            id,
            ".pdf",
        )

    @staticmethod
    def generate_attachment_file_name(id, base_path: str, prefix: str, extension: str, suffix: str = None) -> str:
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
        return "%s_%010d%s" % (prefix, id, suffix)

    @staticmethod
    def generate_insurance_attachment_file_name(insurance: BaseInsurance, extension: str) -> str:
        return InsuranceAttachmentUtils.generate_attachment_file_name(
            insurance.id,
            InsuranceAttachmentUtils.insurance_base_path,
            InsuranceAttachmentUtils.insurance_prefix,
            extension,
        )
