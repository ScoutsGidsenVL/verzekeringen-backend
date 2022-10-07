import logging

from django.conf import settings
from django.core.files.storage import default_storage

from scouts_auth.auth.models import User
from scouts_insurances.equipment.models import Equipment
from scouts_insurances.insurances.models import BaseInsurance, TemporaryInsurance, TemporaryVehicleInsurance, \
    EquipmentInsurance, ActivityInsurance, EventInsurance, GroupSize, TravelAssistanceInsurance
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

    def send_insurance(self, insurance: BaseInsurance, created_by: User):
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
            to=[InsuranceSettingsHelper.get_insurance_requester_address(
                created_by.email, insurance.responsible_member.email
            )],
            add_attachments=True,
            tags=["Verzekeringsaanvraag"]
        )

    def _prepare_insurance_dictionary(self, insurance: BaseInsurance):
        """Replaces the keys in the mail template with the actual values."""
        return {
            "date_of_request": insurance.created_on.strftime("%d-%m-%Y"),
            "title_mail": "",
            "insurance__type": insurance.type.description.lower(),
            "requester__first_name": insurance.responsible_member.first_name,
            "total_price": insurance.total_cost,
            "extra": self._extra_text(insurance),
            "extra_list_items": self._extra_list_items(insurance)
        }

    def _extra_list_items(self, insurance: BaseInsurance) -> str:

        if isinstance(insurance, TemporaryInsurance):
            non_member_list = list()
            for non_member in insurance.non_members.all():
                non_member_list.append(non_member.full_name())
            city = f'<li>Locatie: {insurance.city}</li>' if insurance.city else ""
            return f'<li>Periode: {insurance.start_date.strftime("%d %b %Y")} - {insurance.end_date.strftime("%d %b %Y")}</li>' \
                   f'<li>Aard van activiteit: {insurance.nature}</li>' \
                   f'<li>Land: {insurance.country.name if insurance.country else "België"}</li>' \
                   + city + \
                   f'<li>Deelnemers: {", ".join(non_member_list)}</li>' \
                   f'<li>Opmerkingen: {insurance.comment if insurance.comment else "geen"}</li>'
        elif isinstance(insurance, TemporaryVehicleInsurance):
            driver_list = list()
            for driver in insurance.drivers:
                driver_list.append(driver.full_name())
            insurance_options_list = list()
            for number in str(insurance.insurance_options):
                if number == "1":
                    insurance_options_list.append("Optie 1: Omniumverzekering.")
                if number == "2":
                    insurance_options_list.append("Optie 2: Vrijstelling van eigen omnium dekken.")
                if number == "3":
                    insurance_options_list.append(
                        "Optie 3: Huurvoertuig: vrijstelling verzekering burgerlijke aansprakelijkheid dekken tot 500 euro.")

            return f'<li>Periode: {insurance.start_date.strftime("%d %b %Y")} - {insurance.end_date.strftime("%d %b %Y")}</li>' \
                   f'<li>Bestuurders: {", ".join(driver_list)}</li>' \
                   f'<li>Eigenaar: {insurance.owner.full_name()}</li>' \
                   f'<li>Verzekering opties: {", ".join(insurance_options_list)}</li>' \
                   f'<li>Voertuig: {insurance.vehicle}</li>' \
                   f'<li>Opmerkingen: {insurance.comment if insurance.comment else "geen"}</li>'
        elif isinstance(insurance, EquipmentInsurance):
            city = f'<li>Locatie: {insurance.city}</li>' if insurance.city else ""
            equipment_list = list()
            equipment_list_string = "<ul>"
            for equipment in Equipment.objects.all().filter(insurance_id=insurance.id):
                equipment_list.append(equipment.to_string_mail())
            for item in equipment_list:
                equipment_list_string = equipment_list_string + f"<li>{item}</li>"
            equipment_list_string = equipment_list_string + "</ul>"
            return f'<li>Periode: {insurance.start_date.strftime("%d %b %Y")} - {insurance.end_date.strftime("%d %b %Y")}</li>' \
                   f'<li>Aard van activiteit: {insurance.nature}</li>' \
                   f'<li>Land: {insurance.country.name if insurance.country else "België"}</li>' \
                   + city + \
                   f'<li>Materiaal:  {equipment_list_string}</li>' \
                   f'<li>Opmerkingen: {insurance.comment if insurance.comment else "geen"}</li>'
        elif isinstance(insurance, EventInsurance):
            city = f'<li>Locatie: {insurance.city}</li>' if insurance.city else ""
            event_sizes = {
                1: '1-500 (65,55 eur/dag)',
                2: '500-1000 (131,10 eur/dag)',
                3: '1000-1500 (163,88 eur/dag)',
                4: '1500-2500 (229,43 eur/dag)',
                5: 'meer dan 2500 (in overleg met Ethias)'
            }

            return f'<li>Periode: {insurance.start_date.strftime("%d %b %Y %H:%M")} - {insurance.end_date.strftime("%d %b %Y %H:%M")}</li>' \
                   f'<li>Aard van activiteit: {insurance.nature}</li>' \
                   f'<li>Land: België</li>' \
                   + city + \
                   f'<li>Grootte van evenement:  {event_sizes[insurance.event_size]}</li>' \
                   f'<li>Opmerkingen: {insurance.comment if insurance.comment else "geen"}</li>'
        elif isinstance(insurance, ActivityInsurance):
            city = f'<li>Locatie: {insurance.city}</li>' if insurance.city else ""

            return f'<li>Periode: {insurance.start_date.strftime("%d %b %Y")} - {insurance.end_date.strftime("%d %b %Y")}</li>' \
                   f'<li>Aard van activiteit: {insurance.nature}</li>' \
                   f'<li>Land: België</li>' \
                   + city + \
                   f'<li>Aantal extra te verzekeren personen:  {GroupSize.from_choice(insurance.group_size)[1]}</li>' \
                   f'<li>Opmerkingen: {insurance.comment if insurance.comment else "geen"}</li>'
        elif isinstance(insurance, TravelAssistanceInsurance):
            participants = list()
            for participant in insurance.participants.all():
                participants.append(participant.full_name())
            vehicle = f"<li>Voertuig: {insurance.vehicle_with_simple_trailer_to_str_mail()}</li>" if insurance.vehicle else ""
            return f'<li>Periode: {insurance.start_date.strftime("%d %b %Y")} - {insurance.end_date.strftime("%d %b %Y")}</li>' \
                   f'<li>Land: {insurance.country if insurance.country else "België"}</li>' \
                   f'<li>Deelnemers: {", ".join(participants)}</li>' \
                   + vehicle + \
                   f'<li>Opmerkingen: {insurance.comment if insurance.comment else "geen"}</li>'
        return ''

    def _extra_text(self, insurance: BaseInsurance) -> str:

        # frontend_base_url = settings.FRONTEND_BASE_URL #USE THIS ENV VAR FOR LOCAL
        frontend_base_url = settings.BASE_URL  # USE THIS ENV VAR FOR ACC AND PROD
        if (insurance.type.description.lower() == 'eenmalige activiteit') or (
                insurance.type.description.lower() == 'evenementen verzekering'):
            return f"<div>&nbsp;</div>Vergeet niet om na de activiteit <a style='text-decoration: underline;' href='https://www.scoutsengidsenvlaanderen.be/media/1317/download'>de deelnemerslijst</a> in te vullen en te bezorgen, ook als er geen ongeval gebeurde. Je kan het in <a style='text-decoration: underline;' href='{frontend_base_url}/#/eenmalige-activiteit-detail/{insurance.id}'>je aanvraag</a> opladen.<div>&nbsp;</div>"

        if insurance.type.description.lower() == 'autoverzekering':
            # return f"<div>&nbsp;</div>Voor eigen voertuigen kan Ethias deze aanvraag pas goedkeuren na ontvangst van het ingevulde expertiseverslag. Voor gehuurde voertuigen kan Scouts en Gidsen Vlaanderen deze aanvraag pas goedkeuren na ontvangst van het huurcontract met beschrijving van de staat van het voertuig. Je kan het in <a style='text-decoration: underline;' href='{frontend_base_url}/#/eenmalige-activiteit-detail/{insurance.id}'>je aanvraag</a> opladen.<div>&nbsp;</div>"
            return f"<div>&nbsp;</div>Ten vroegste 2 werkdagen en minimum 1 werkdag voor je op scoutsactiviteit vertrekt moet je online het <a style='text-decoration: underline;' href='https://forms.office.com/Pages/ResponsePage.aspx?id=_EiNAphkiESNwUyecUlr-F2-J9LUk9NNsZ0o6D7lSvhUN1pGQ1k5NDNWT1ZCTDFVUDdFT09ZQk9XRSQlQCN0PWcu'>expertiseformulier</a> van Ethias invullen. Meer uitleg over deze procedure vind je <a style='text-decoration: underline;' href='https://www.scoutsengidsenvlaanderen.be/leiding/ondersteuning/groepsleiding/verzekeringen/autoverzekering#expertiseformulier'>op onze website</a>.<div>&nbsp;</div>"

        return '<div>&nbsp;</div>'

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
            bcc: list = settings.EMAIL_INSURANCE_BCC,
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
