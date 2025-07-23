import json
import logging

from django.conf import settings

from apps.people.models import InuitsClaimVictim
from apps.insurances.utils import InuitsInsuranceSettingsHelper
from apps.insurances.models import (
    InsuranceClaim,
    InsuranceClaimAttachment,
)

from scouts_insurances.insurances.services import InsuranceMailService

from scouts_auth.inuits.mail import Email, EmailAttachment
from scouts_auth.inuits.utils import TextUtils

logger = logging.getLogger(__name__)


class InuitsInsuranceMailService(InsuranceMailService):
    """
    Prepares claims mails and sends them.

    #82929, #80695:
    The claim report (pdf) and all attachments should be sent to:
    - The insurance company
    - The afflicted member (or his/her parents) -> email address in claim
    #80697:
    - The declarant should be notified a claim was reported
    """

    from_email = InuitsInsuranceSettingsHelper.get_email_insurance_from()
    template_path_start = settings.RESOURCES_MAIL_TEMPLATE_START
    template_path_end = settings.RESOURCES_MAIL_TEMPLATE_END

    insurer_template_path = settings.RESOURCES_CLAIMS_INSURER_TEMPLATE_PATH
    insurer_subject = "Aangifte schade van (((date_of_accident)))"
    insurer_address = ""

    victim_template_path = settings.RESOURCES_CLAIMS_VICTIM_TEMPLATE_PATH
    victim_subject = "Bevestiging aangifte schade van (((date_of_accident)))"

    stakeholder_template_path = settings.RESOURCES_CLAIMS_STAKEHOLDER_TEMPLATE_PATH
    stakeholder_subject = "Bevestiging aangifte schade van (((date_of_accident)))"

    def send_claim(
        self,
        claim: InsuranceClaim,
        claim_report_path: str,
    ):
        self.notify_insurer(claim, claim_report_path)
        self.notify_victim(claim, claim_report_path)
        self.notify_stakeholder(claim)

    def notify_insurer(self, claim: InsuranceClaim, claim_report_path: str):
        """Send the claim to the insurer."""
        logger.debug("Preparing to send claim #%d to the insurer", claim.id)

        subject = self.insurer_subject
        subject = subject.replace("(((claim.id)))", str(claim.id))
        subject = subject.replace("(((date_of_accident)))", str(claim.date_of_accident.strftime("%d-%m-%Y")).lower())

        template_id = settings.SENDINBLUE_TEMPLATE_INSURANCE_INSURER

        self._send_prepared_claim_email(
            claim=claim,
            subject=subject,
            template_path=self.insurer_template_path,
            to=[InuitsInsuranceSettingsHelper.get_insurer_address(self.insurer_address, claim.declarant.email)],
            add_attachments=True,
            template_id=template_id,
            claim_report_path=claim_report_path,
            tags=["Schadeaangifte"],
        )

    def notify_victim(self, claim: InsuranceClaim, claim_report_path: str):
        """Notify the victim that the claim was sent to the insurer."""
        logger.debug("Preparing to send claim #%d to the victim", claim.id)

        subject = self.victim_subject
        subject = subject.replace("(((date_of_accident)))", str(claim.date_of_accident.strftime("%d-%m-%Y")).lower())

        victim: InuitsClaimVictim = claim.victim

        template_id = settings.SENDINBLUE_TEMPLATE_INSURANCE_VICTIM

        self._send_prepared_claim_email(
            claim=claim,
            subject=subject,
            template_path=self.victim_template_path,
            to=[InuitsInsuranceSettingsHelper.get_victim_email(victim.email, claim.declarant.email)],
            add_attachments=True,
            template_id=template_id,
            claim_report_path=claim_report_path,
            tags=["Schadeaangifte"],
        )

    def notify_stakeholder(self, claim: InsuranceClaim):
        """Notify the stakeholder that a claim was sent to the insurer and victim."""
        logger.debug("Preparing to notify the stakeholder about claim #%d", claim.id)

        subject = self.stakeholder_subject
        subject = subject.replace("(((claim.id)))", str(claim.id))
        subject = subject.replace("(((date_of_accident)))", str(claim.date_of_accident.strftime("%d-%m-%Y")).lower())

        template_id = settings.SENDINBLUE_TEMPLATE_INSURANCE_DECLERANT

        self._send_prepared_claim_email(
            claim=claim,
            subject=subject,
            template_path=self.stakeholder_template_path,
            to=[InuitsInsuranceSettingsHelper.get_declarant_email(claim.declarant.email, claim.declarant.email)],
            template_id=template_id,
            add_attachments=False,
            tags=["Schadeaangifte"],
        )

    def _prepare_claim_dictionary(self, claim: InsuranceClaim, via_blue: bool = False, template_id: int = None) -> dict:
        """
        ...
        Consider both django mail templates and Sendinblue templates.
        """
        if via_blue:
            params = {}
            if template_id == settings.SENDINBLUE_TEMPLATE_INSURANCE_VICTIM:
                params["voornaam"] = claim.victim.first_name
            elif template_id == settings.SENDINBLUE_TEMPLATE_INSURANCE_DECLERANT:
                accident_date = (
                    claim.date_of_accident
                    and claim.date_of_accident.strftime("%d-%m-%Y")
                )
                create_date = claim.created_on.strftime("%d-%m-%Y")
                params["voornaam"] = claim.declarant.first_name
                params["details"] = (
                    f"<li>Aangever: {claim.declarant.first_name}</li>"
                    f"<li>Slachtoffer: {claim.victim.first_name}</li>"
                    f"<li>Datum ongeval: {accident_date or ''}</li>"
                    f"<li>Datum aangifte: {create_date}</li>"
                )
            return params
        return {
            "declarant__first_name": claim.declarant.first_name,
            "declarant__name": claim.declarant.first_name + " " + claim.declarant.last_name,
            "victim__first_name": claim.victim.first_name,
            "victim__name": claim.victim.first_name + " " + claim.victim.last_name,
            "victim__email": claim.victim.email,
            "date_of_accident": claim.date_of_accident.date().strftime("%d-%m-%Y"),
            "date_of_declaration": claim.created_on.date().strftime("%d-%m-%Y"),
            "title_mail--": "",
        }

    def _prepare_email_body(self, template_path: str, dictionary: dict) -> str:
        return TextUtils.replace(
            path=template_path, dictionary=dictionary, placeholder_start="--", placeholder_end="--"
        )

    def _send_prepared_claim_email(
        self,
        claim: InsuranceClaim,
        subject: str,
        template_path: str,
        to: list = None,
        cc: list = None,
        bcc: list = None,
        reply_to: str = None,
        template_id: int = None,
        claim_report_path: str = None,
        add_attachments: bool = False,
        tags=None,
    ):
        if tags is None:
            tags = []

        if not reply_to:
            reply_to = InuitsInsuranceSettingsHelper.get_email_insurance_reply_to(self.from_email)

        values = self._prepare_claim_dictionary(claim, settings.USE_SENDINBLUE, template_id)

        mail = Email(
            subject=subject,
            from_email=self.from_email,
            to=to,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            template_id=template_id,
        )

        if settings.USE_SENDINBLUE:
            mail.body = json.dumps(values)
        else:
            mail.is_html = True
            html_body = self._prepare_email_body(template_path, values)
            html_body = TextUtils.compose_html_email(
                self.template_path_start, html_body, self.template_path_end
            )
            mail.html_body = html_body

        if add_attachments:
            if claim_report_path:
                mail.add_attachment(EmailAttachment(claim_report_path))
            if claim.has_attachment():
                attachment: InsuranceClaimAttachment = claim.attachment
                logger.debug("Adding attachment with path %s to claim(%d) email", attachment.file.file.name, claim.id)
                mail.add_attachment(EmailAttachment(attachment.file.file.name, self.file_service))

        self.send(mail, tags=tags)
