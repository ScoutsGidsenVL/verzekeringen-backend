from django.db import models
from django.core.validators import FileExtensionValidator
from apps.insurances.models.insurance_claim import InsuranceClaim
from inuits.models import BaseModel


class InsuranceClaimAttachment(BaseModel):
    file = models.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "jpg",
                    "jpeg",
                    "png",
                    "gif",
                    "bmp",
                    "webp",
                    "tiff",
                    "odt",
                    "pptx",
                    "docx",
                    "pdf",
                    "doc",
                    "xls",
                ]
            )
        ],
    )
    insurance_claim = models.OneToOneField(InsuranceClaim, on_delete=models.CASCADE, related_name="attachment")
    content_type = models.CharField(max_length=100)

    def delete(self, using=None, keep_parents=False):
        storage = self.file.storage

        if storage.exists(self.file.name):
            storage.delete(self.file.name)

        super().delete(using=using, keep_parents=keep_parents)
