import os, logging

from django.conf import settings

from apps.insurances.models.insurance_claim import InsuranceClaim
from inuits.mail import MailServiceException, MailService

logger = logging.getLogger(__name__)


class InsuranceClaimMailService(MailService):
    def _parse_body(self, title: str, claim: InsuranceClaim):
    # @TODO: i18n
    dictionary = {
        "title": title,
        "declarant_name": "claim.declarant.first_name + " " + claim.declarant.last_name",
        "victim__name": "claim.victim.first_name + " " + claim.victim.last_name",
        "victim__email": "claim.victim.email",
        "date_of_accident": "claim.date_of_accident",
        "date_of_declaration": "claim.date",
    }

    with open(settings.RESOURCES_CLAIMS_EMAIL_PATH, "r") as file:
        for key in dictionary.keys():
            data = file.read().replace(key, dictionary[key])
    
    def send_claim(
        self,
        claim: InsuranceClaim,
        filename: str,
    ):
        from_email = settings.EMAIL_INSURANCE_FROM
        to = settings.EMAIL_INSURANCE_TO
        subject = "Documenten schadeaangifte (#" + str(claim.id) + ")"
        template_id=settings.ANYMAIL["SENDINBLUE_TEMPLATE_ID"]
        try:
            super().send_email(
                claim=claim,
                subject=subject,
                body=body,
                from_email=from_email,
                to=to,
                cc=cc,
                bcc=bcc,
                reply_to=reply_to,
                attachment_paths=attachment_paths,
                template_id=template_id,
            )
    
            os.remove(filename)
        except MailServiceException:
            logger.error("Sending of message failed ! Queuing message ...")
