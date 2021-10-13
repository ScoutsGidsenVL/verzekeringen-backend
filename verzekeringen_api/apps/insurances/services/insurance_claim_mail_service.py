import logging

from django.conf import settings

from apps.insurances.models import InsuranceClaim, InsuranceClaimAttachment
from inuits.mail import Email, EmailAttachment, EmailService
from inuits.files import FileService
from inuits.utils import TextUtils

logger = logging.getLogger(__name__)


class InsuranceClaimMailService(EmailService):
    """
    Prepares claims mails and sends them.

    #82929, #80695:
    The claim report (pdf) and all attachments should be sent to:
    - The insurance company
    - The afflicted member (or his/her parents) -> email address in claim
    #80697:
    - The group leader should be notified a claim was reported
    """

    from_email = settings.EMAIL_INSURANCE_FROM
    to = settings.EMAIL_INSURANCE_TO

    email_path = settings.RESOURCES_CLAIMS_EMAIL_PATH
    email_subject = "Documenten schadeaangifte (#{{ claim.id }})"

    email_notification_path = settings.RESOURCES_CLAIMS_EMAIL_NOTIFICATION_PATH
    email_notificaton_subject = "Schadeaangifte (#{{ claim.id }})"

    template_id = settings.EMAIL_TEMPLATE

    file_service = FileService()
    mail_service = EmailService()

    def send_claim(
        self,
        claim: InsuranceClaim,
        claim_report_path: str,
    ):
        # TODO: load group leader from GA
        stakeholder = self.to

        self.report_claim(claim=claim, claim_report_path=claim_report_path)
        self.notify_stakeholders(claim=claim, stakeholder=stakeholder)

        #     os.remove(filename)
        # except MailServiceException:
        #     logger.error("(CLAIM %s) Sending of message failed ! Queuing message ...", claim.id)

    def report_claim(self, claim: InsuranceClaim, claim_report_path: str):
        """Reports the claim to the insurance company and member/parents."""

        dictionary = self._prepare_dictionary(claim)
        body = self._prepare_email_body(self.email_path, dictionary)

        to = self.to
        # to.append(claim.declarant.email)
        to.append(claim.victim.email)

        logger.debug("Preparing to send claim(%d) to insurer and member", claim.id)
        logger.debug("Receivers: %s", ", ".join(to))

        mail = Email(
            subject=dictionary["subject"],
            body=body,
            from_email=self.from_email,
            to=to,
            reply_to=self.from_email,
            template_id=self.template_id,
        )

        mail.add_attachment(EmailAttachment(claim_report_path))
        if claim.has_attachment():
            attachment: InsuranceClaimAttachment = claim.attachment
            logger.debug("Adding attachment with path %s to claim(%d) email", attachment.get_path(), claim.id)
            mail.add_attachment(EmailAttachment(attachment.get_path(), self.file_service))

        self.mail_service.send(mail)

    def notify_stakeholders(self, claim: InsuranceClaim, stakeholder: str):
        """Notifies the group leader of the reported claim."""
        dictionary = self._prepare_dictionary(claim)
        # Name of the group leader
        dictionary["stakeholder_name"] = stakeholder
        body = self._prepare_email_body(self.email_notification_path, dictionary)

        mail = Email(
            subject=dictionary["subject"],
            body=body,
            from_email=self.from_email,
            to=stakeholder,
            reply_to=self.from_email,
            attachment_paths=None,
            template_id=self.template_id,
        )

    def _prepare_dictionary(self, claim: InsuranceClaim):
        """Replaces the keys in the mail template with the actual values."""
        subject = self.email_subject.replace("{{ claim.id }}", str(claim.id))

        # @TODO: i18n
        return {
            "subject": subject,
            "declarant_name": claim.declarant.first_name + " " + claim.declarant.last_name,
            "victim__name": claim.victim.first_name + " " + claim.victim.last_name,
            "victim__email": claim.victim.email,
            "date_of_accident": claim.date_of_accident,
            "date_of_declaration": claim.date,
        }

    def _prepare_email_body(self, path: str, dictionary: dict) -> str:
        return TextUtils.replace(path=path, dictionary=dictionary)
