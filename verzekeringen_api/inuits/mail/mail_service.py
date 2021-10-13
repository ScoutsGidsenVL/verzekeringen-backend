import logging

from django.conf import settings
from django.core.mail import EmailMessage
from anymail.message import AnymailMessage

from inuits.mail import Email

logger = logging.getLogger(__name__)


class EmailService:

    backend = settings.EMAIL_BACKEND

    def send(self, mail: Email):
        return self.send_email(
            subject=mail.subject,
            body=mail.body,
            from_email=mail.from_email,
            to=mail.to,
            cc=mail.cc,
            bcc=mail.bcc,
            reply_to=mail.reply_to,
            attachment_paths=mail.attachment_paths,
            template_id=mail.template_id,
            attachments=mail.attachments,
        )

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
        attachments: list = None,
    ):
        logger.debug("Sending mail through backend %s", self.backend)

        if self.backend == "anymail.backends.sendinblue.EmailBackend":
            return self.send_send_in_blue_email(
                body=body,
                subject=subject,
                from_email=from_email,
                to=to,
                attachment_paths=attachment_paths,
                template_id=template_id,
                attachments=attachments,
            )
        else:
            return self.send_django_email(
                body=body,
                subject=subject,
                from_email=from_email,
                to=to,
                attachment_paths=attachment_paths,
                attachments=attachments,
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
        attachments: list = None,
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

        attachment_paths_len = len(attachment_paths)
        if attachment_paths and attachment_paths_len > 0:
            logger.debug("Adding %d attachments to email", attachment_paths_len)
            for attachment_path in attachment_paths:
                message.attach_file(attachment_path)
        attachments_len = len(attachments)
        if attachments and attachments_len > 0:
            logger.debug("Adding %d attachments to email", attachments_len)
            for attachment in attachments:
                message.attach_file(attachment.as_attachment())


        try:
            message.send()
        except Exception as exc:
            # Actually do something when this fails
            # https://redmine.inuits.eu/issues/83311
            logger.error("Mail could not be sent", exc)

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
        attachments: list = None,
    ):
        message = AnymailMessage(
            subject="Welcome",
            body="Welcome to our site",
            from_email=from_email,
            to=to,
            tags=["Schadeclaim"],  # Anymail extra in constructor
        )

        if attachment_paths:
            for attachment_path in attachment_paths:
                message.attach_file(attachment_path)
        if attachments:
            for attachment in attachments:
                message.attach_file(attachment.as_attachment())

        message.send()

        logger.debug("Mail status: %s", message.anymail_status)
