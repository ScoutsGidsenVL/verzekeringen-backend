import logging

from django.conf import settings
from django.core.files.storage import default_storage

from scouts_insurances.insurances.models import BaseInsurance
from scouts_insurances.insurances.utils import InsuranceSettingsHelper

from scouts_auth.inuits.mail import Email, EmailService
from scouts_auth.inuits.utils import TextUtils

logger = logging.getLogger(__name__)


class InsuranceMailService(EmailService):
    """
    Prepares claims mails and sends them.

    #82929, #80695:
    The claim report (pdf) and all attachments should be sent to:
    - The insurance company
    - The afflicted member (or his/her parents) -> email address in claim
    #80697:
    - The declarant should be notified a claim was reported
    """

    from_email = InsuranceSettingsHelper.get_email_insurance_from()
    template_path_start = settings.RESOURCES_MAIL_TEMPLATE_START
    template_path_end = settings.RESOURCES_MAIL_TEMPLATE_END

    insurance_request_template_path = settings.RESOURCES_INSURANCES_TEMPLATE_PATH
    insurance_request_subject = "Bevestiging aanvraag (((insurance__type))) van (((insurance__start_date))) tot (((insurance__end_date)))"
    insurance_request_address = ""

    file_service = default_storage

    def send_insurance(self, insurance: BaseInsurance):
        """Send the claim to the insurer."""
        logger.debug(
            "Preparing to send insurance request confirmation #%d to requester %s",
            insurance.id,
            insurance.responsible_member.first_name + " " + insurance.responsible_member.last_name,
        )

        dictionary = self._prepare_insurance_dictionary(insurance)

        subject = self.insurance_request_subject
        subject = subject.replace("(((insurance__type)))", str(insurance.type.description).lower())
        subject = subject.replace("(((insurance__start_date)))", str(insurance.start_date.strftime("%d-%m-%Y")).lower())
        subject = subject.replace("(((insurance__end_date)))", str(insurance.end_date.strftime("%d-%m-%Y")).lower())

        self._send_prepared_insurance_email(
            insurance=insurance,
            dictionary=dictionary,
            subject=subject,
            template_path=self.insurance_request_template_path,
            to=InsuranceSettingsHelper.get_insurance_requester_address(
                self.insurance_request_address, insurance.responsible_member.email
            ),
            add_attachments=True,
            tags=["Verzekeringsaanvraag"]
        )

    def _prepare_insurance_dictionary(self, insurance: BaseInsurance):
        """Replaces the keys in the mail template with the actual values."""
        return {
            "date_of_request": insurance.created_on.date(),
            "title_mail": "",
            "insurance__type": insurance.type.description.lower(),
            "requester__first_name": insurance.responsible_member.first_name,
            "total_price": insurance.total_cost,
        }

    def _prepare_email_body(self, template_path: str, dictionary: dict) -> str:
        return TextUtils.replace(
            path=template_path, dictionary=dictionary, placeholder_start="--", placeholder_end="--"
        )

    def _send_prepared_insurance_email(
            self,
            insurance: BaseInsurance,
            dictionary: dict,
            subject: str,
            template_path: str,
            to: list = None,
            cc: list = None,
            bcc: list = None,
            reply_to: str = None,
            template_id: str = None,
            add_attachments: bool = False,
            tags=None
    ):
        if tags is None:
            tags = []
        dictionary["title_mail"] = subject
        body = None
        html_body = self._prepare_email_body(template_path, dictionary)
        html_body = TextUtils.compose_html_email(self.template_path_start, html_body, self.template_path_end)

        if not reply_to:
            reply_to = self.from_email

        mail = Email(
            subject=subject,
            body=body,
            html_body=html_body,
            from_email=self.from_email,
            to=to,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            template_id=template_id,
            is_html=True,
        )

        # if add_attachments:
        #     if insurance.has_attachment():
        #         attachment = None
        #         if insurance.type.is_activity_insurance():
        #             attachment: ActivityInsuranceAttachment = insurance.attachment
        #         elif insurance.type.is_event_insurance():
        #             attachment: EventInsuranceAttachment = insurance.attachment

        #         if not attachment:
        #             logger.error("Unable to append attachment for insurance with id %d", insurance.id)
        #         else:
        #             logger.debug(
        #                 "Adding attachment with path %s to insurance(%d) email", attachment.file.name, insurance.id
        #             )
        #             mail.add_attachment(EmailAttachment(attachment.file.name, self.file_service))

        self.send(mail, tags=tags)
