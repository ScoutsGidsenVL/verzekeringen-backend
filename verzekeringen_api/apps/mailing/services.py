import logging
from django.conf import settings
from django.core.mail import EmailMessage
from anymail.message import AnymailMessage

from apps.insurances.models.insurance_claim import InsuranceClaim
from apps.base.exceptions import MailServiceException

logger = logging.getLogger(__name__)


class MailService:
    # Example method that might be handy when sending send in blue emails
    # Not tested but should work
    def send_email(
        self,
        subject: str = "",
        body: str = "",
        from_email: str = None,
        to: list = None,
        cc: list = None,
        bcc: list = None,
        reply_to: str = None,
        attachment_paths: list = None,
        template_id=None,
    ):
        if settings.EMAIL_BACKEND == "anymail.backends.sendinblue.EmailBackend":
            self.send_send_in_blue_email(
                body=body,
                subject=subject,
                from_email=from_email,
                to=to,
                attachment_paths=attachment_paths,
                template_id=template_id,
            )
        else:
            self.send_django_email(
                body=body,
                subject=subject,
                from_email=from_email,
                to=to,
                attachment_paths=attachment_paths,
            )

    def send_django_email(
        self,
        subject: str = "",
        body: str = "",
        from_email: str = None,
        to: list = None,
        cc: list = None,
        bcc: list = None,
        reply_to: str = None,
        attachment_paths: list = None,
    ):
        if reply_to is None:
            reply_to = from_email

        message = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=to,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
        )

        for attachment_path in attachment_paths:
            message.attach_file(attachment_path)

        try:
            logger.debug("Sending mail to (%s)", ", ".join(to))
            message.send()
        except Exception as e:
            print(e)
            # Actually do something when this fails
            # https://redmine.inuits.eu/issues/83311
            logger.error("Mail could not be sent")

    def send_send_in_blue_email(
        self,
        subject: str = "",
        body: str = "",
        from_email: str = None,
        to: list = None,
        cc: list = None,
        bcc: list = None,
        reply_to: str = None,
        attachment_paths: list = None,
        template_id=None,
    ):
        message = AnymailMessage(
            subject="Welcome",
            body="Welcome to our site",
            to=to,
            tags=["Schadeclaim"],  # Anymail extra in constructor
        )

        for attachment_path in attachment_paths:
            message.attach_file(attachment_path)

        message.send()

        logger.debug("Mail status: %s", message.anymail_status)


class InsuranceClaimMailService(MailService):
    def send_claim(
        self,
        claim: InsuranceClaim,
        attachment_paths: list = [],
        template_id: str = None,
    ):
        subject = ""

        super().send_email()
