import logging

from django.conf import settings

from apps.insurances.models import InsuranceClaim


logger = logging.getLogger(__name__)


class InsuranceClaimFileUtils:

    static_setup = False

    insurance_base_path = settings.INSURANCE_FILES_BASE_PATH
    insurance_prefix = settings.INSURANCE_CLAIM_FILE_NAME_PREFIX

    claim_base_path = settings.INSURANCE_CLAIM_FILES_BASE_PATH
    claim_prefix = settings.INSURANCE_CLAIM_FILE_NAME_PREFIX
    claim_suffix = settings.INSURANCE_CLAIM_FILE_NAME_SUFFIX

    @staticmethod
    def _clean(input: str, search: str, replace: str):
        return input.replace(search, replace)

    @staticmethod
    def _static_setup():
        if not InsuranceClaimFileUtils.static_setup:
            if InsuranceClaimFileUtils.insurance_base_path[-1] != "/":
                logger.warn("INSURANCES_FILES_BASE_PATH should end with a slash")
                InsuranceClaimFileUtils.insurance_base_path = InsuranceClaimFileUtils.insurance_base_path + "/"
            if InsuranceClaimFileUtils.claim_base_path[-1] != "/":
                logger.warn("INSURANCE_CLAIM_FILES_BASE_PATH should end with a slash")
                InsuranceClaimFileUtils.claim_base_path = InsuranceClaimFileUtils.claim_base_path + "/"

            InsuranceClaimFileUtils.insurance_prefix = InsuranceClaimFileUtils._clean(
                InsuranceClaimFileUtils.insurance_prefix, " ", "_"
            )
            InsuranceClaimFileUtils.claim_prefix = InsuranceClaimFileUtils._clean(
                InsuranceClaimFileUtils.claim_prefix, " ", "_"
            )
            InsuranceClaimFileUtils.claim_suffix = InsuranceClaimFileUtils._clean(
                InsuranceClaimFileUtils.claim_suffix, " ", "_"
            )

    @staticmethod
    def generate_claim_report_file_name(claim: InsuranceClaim) -> str:
        InsuranceClaimFileUtils._static_setup()

        return "%s%s_%010d%s" % (
            InsuranceClaimFileUtils.insurance_base_path,
            InsuranceClaimFileUtils.insurance_prefix,
            claim.id,
            ".pdf",
        )

    @staticmethod
    def get_claim_base_path() -> str:
        InsuranceClaimFileUtils._static_setup()

        return InsuranceClaimFileUtils.claim_base_path

    @staticmethod
    def generate_claim_report_temp_file_name(claim: InsuranceClaim) -> str:
        InsuranceClaimFileUtils._static_setup()

        return "%s_%010d%s" % (InsuranceClaimFileUtils.insurance_prefix, claim.id, ".pdf")

    @staticmethod
    def generate_claim_attachment_file_name(claim: InsuranceClaim, extension: str) -> str:
        InsuranceClaimFileUtils._static_setup()

        return "%s%s_%010d_%s%s" % (
            InsuranceClaimFileUtils.claim_base_path,
            InsuranceClaimFileUtils.claim_prefix,
            claim.id,
            InsuranceClaimFileUtils.claim_suffix,
            extension,
        )
