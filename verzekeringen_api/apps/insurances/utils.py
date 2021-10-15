from django.conf import settings

from apps.insurances.models import InsuranceClaim


class InsuranceClaimFileUtils:

    insurance_base_path = settings.INSURANCE_FILES_BASE_PATH
    insurance_prefix = settings.INSURANCE_CLAIM_FILE_NAME_PREFIX

    claim_base_path = settings.INSURANCE_CLAIM_FILES_BASE_PATH
    claim_prefix = settings.INSURANCE_CLAIM_FILE_NAME_PREFIX
    claim_suffix = settings.INSURANCE_CLAIM_FILE_NAME_SUFFIX

    @staticmethod
    def generate_claim_report_file_name(claim: InsuranceClaim) -> str:
        return "%s%s_%010d%s" % (
            InsuranceClaimFileUtils.insurance_base_path,
            InsuranceClaimFileUtils.insurance_prefix,
            claim.id,
            ".pdf",
        )

    @staticmethod
    def generate_claim_report_temp_file_name(claim: InsuranceClaim) -> str:
        return "%s%010d%s" % (InsuranceClaimFileUtils.insurance_prefix, claim.id, ".pdf")

    @staticmethod
    def generate_claim_attachment_file_name(claim: InsuranceClaim, extension: str) -> str:
        return "%s%s_%010d_%s%s" % (
            InsuranceClaimFileUtils.claim_base_path,
            InsuranceClaimFileUtils.claim_prefix,
            claim.id,
            InsuranceClaimFileUtils.claim_suffix,
            extension,
        )
