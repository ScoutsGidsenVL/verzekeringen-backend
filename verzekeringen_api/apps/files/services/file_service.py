from django.core.files.base import File
from ..models import InsuranceClaimAttachment


def store_attachment(*, uploaded_file: File, claim: InsuranceClaimAttachment) -> InsuranceClaimAttachment:
    print(uploaded_file)
    attachment = InsuranceClaimAttachment()
    attachment.insurance_claim = claim
    attachment.file.save(name=uploaded_file.name, content=uploaded_file)
    attachment.content_type = uploaded_file.content_type
    attachment.full_clean()
    attachment.save()

    return attachment
