import logging
import json
import re

from django.conf import settings
from django.core.files.storage import default_storage

from scouts_auth.auth.models import User
from scouts_insurances.equipment.models import Equipment
from scouts_insurances.insurances.models import (
    BaseInsurance,
    TemporaryInsurance,
    TemporaryVehicleInsurance,
    EquipmentInsurance,
    ActivityInsurance,
    EventInsurance,
    GroupSize,
    TravelAssistanceInsurance,
)
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

    file_service = default_storage

    def send_insurance(self, insurance: BaseInsurance, created_by: User):
        """Send the claim to the insurer."""
        logger.debug(
            "Preparing to send insurance request confirmation #%d to requester %s",
            insurance.id,
            insurance.responsible_member.first_name + " " + insurance.responsible_member.last_name,
        )

        subject = "Bevestiging aanvraag {} van {} tot {} [Ref {}]".format(
            str(insurance.type.description).lower(),
            insurance.start_date.strftime("%d-%m-%Y"),
            insurance.end_date.strftime("%d-%m-%Y"),
            insurance.id,
        )

        self._send_prepared_insurance_email(
            insurance=insurance,
            subject=subject,
            template_path=self.insurance_request_template_path,
            to=[
                InsuranceSettingsHelper.get_insurance_requester_address(
                    created_by.email, insurance.responsible_member.email
                )
            ],
            add_attachments=True,
            tags=["Verzekeringsaanvraag"],
        )

    def _prepare_insurance_dictionary(
        self,
        insurance: BaseInsurance,
        via_blue: bool = False
    ):
        """Replaces the keys in the mail template with the actual values.
        Consider both django mail templates and Sendinblue templates.
        """
        if via_blue:
            # Based on template SENDINBLUE_TEMPLATE_INSURANCE_REQUESTER.
            return {
                "voornaam": insurance.responsible_member.first_name,
                "verzekeringstype": insurance.type.description.lower(),
                "extra": self._extra_text(insurance),
                "details": self._extra_list_items(insurance),
            }

        return {
            "date_of_request": insurance.created_on.strftime("%d-%m-%Y"),
            "title_mail": "",
            "insurance__type": insurance.type.description.lower(),
            "requester__first_name": insurance.responsible_member.first_name,
            "total_price": insurance.total_cost,
            "extra": self._extra_text(insurance),
            "extra_list_items": self._extra_list_items(insurance),
        }

    def _extra_list_items(self, insurance: BaseInsurance) -> str:
        if isinstance(insurance, TemporaryInsurance):
            non_member_list = "<ul>"
            for non_member in insurance.non_members.all():
                non_member_list = (
                    non_member_list
                    + f"<li>{non_member.full_name()} {non_member.street} {non_member.number} {f'Bus {non_member.letter_box}' if non_member.letter_box else ''} {non_member.postal_code} {non_member.city} {non_member.birth_date.strftime('%d %b %Y') if non_member.birth_date else ''} {f'Opmerking: {non_member.comment}' if non_member.comment else ''}</li>"
                )
            non_member_list = non_member_list + "</ul>"
            city = f"<li>Locatie: {insurance.city}</li>" if insurance.city else ""
            return (
                f"<li>Periode: {insurance.start_date.strftime('%d %b %Y')} - {insurance.end_date.strftime('%d %b %Y')}</li>"
                f"<li>Aard van activiteit: {insurance.nature}</li>"
                f"<li>Land: {insurance.country.name if insurance.country else 'België'}</li>"
                + city
                + f"<li>Deelnemers: {non_member_list}</li>"
                f"<li>Opmerkingen: {insurance.comment if insurance.comment else 'geen'}</li>"
            )
        elif isinstance(insurance, TemporaryVehicleInsurance):
            driver_list = list()
            for driver in insurance.drivers:
                driver_list.append(driver.full_name())
            insurance_options_list = "<ul>"
            max_coverage = ""
            if insurance.max_coverage:
                if insurance.max_coverage == "A":
                    max_coverage = "vrijstelling dekken tot 250 EUR"
                if insurance.max_coverage == "B":
                    max_coverage = "vrijstelling dekken tot 500 EUR"
                if insurance.max_coverage == "C":
                    max_coverage = "vrijstelling dekken tot 750 EUR"

            for number in str(insurance.insurance_options):
                if number == "1":
                    insurance_options_list = insurance_options_list + "<li>Optie 1: Omniumverzekering.</li>"
                if number == "2":
                    insurance_options_list = (
                        insurance_options_list + "<li>Optie 2: Vrijstelling van eigen omnium "
                        f"dekken. {max_coverage}</li>"
                    )
                if number == "3":
                    insurance_options_list = (
                        insurance_options_list + "<li>Optie 3: Huurvoertuig: vrijstelling "
                        "verzekering burgerlijke aansprakelijkheid "
                        "dekken tot 500 euro.</li> "
                    )
            insurance_options_list = insurance_options_list + "</ul>"
            return (
                f"<li>Periode: {insurance.start_date.strftime('%d %b %Y')} - {insurance.end_date.strftime('%d %b %Y')}</li>"
                f"<li>Bestuurders: {', '.join(driver_list)}</li>"
                f"<li>Eigenaar: {insurance.owner.full_name()} {insurance.owner.street} {insurance.owner.number}  {f'Bus {insurance.owner.letter_box}' if insurance.owner.letter_box else ''} {insurance.owner.postal_code} {insurance.owner.city} {insurance.owner.phone_number} {f'Opmerking: {insurance.owner.comment}' if insurance.owner.comment else ''}</li>"
                f"<li>Gekozen verzekering: {insurance_options_list}</li>"
                f"<li>Voertuig: {insurance.vehicle.vehicle_to_str_mail()}</li>"
                f"<li>Opmerkingen: {insurance.comment if insurance.comment else 'geen'}</li>"
            )
        elif isinstance(insurance, EquipmentInsurance):
            city = f"<li>Locatie: {insurance.city}</li>" if insurance.city else ""
            equipment_list = list()
            equipment_list_string = "<ul>"
            for equipment in Equipment.objects.all().filter(insurance_id=insurance.id):
                equipment_list.append(equipment.to_string_mail())
            for item in equipment_list:
                equipment_list_string = equipment_list_string + f"<li>{item}</li>"
            equipment_list_string = equipment_list_string + "</ul>"
            return (
                f"<li>Periode: {insurance.start_date.strftime('%d %b %Y')} - {insurance.end_date.strftime('%d %b %Y')}</li>"
                f"<li>Aard van activiteit: {insurance.nature}</li>"
                f"<li>Land: {insurance.country.name if insurance.country else 'België'}</li>"
                + city
                + f"<li>Materiaal:  {equipment_list_string}</li>"
                f"<li>Opmerkingen: {insurance.comment if insurance.comment else 'geen'}</li>"
            )
        elif isinstance(insurance, EventInsurance):
            city = f"<li>Locatie: {insurance.city}</li>" if insurance.city else ""
            event_sizes = {
                1: "1-500 (65,55 eur/dag)",
                2: "500-1000 (131,10 eur/dag)",
                3: "1000-1500 (163,88 eur/dag)",
                4: "1500-2500 (229,43 eur/dag)",
                5: "meer dan 2500 (in overleg met Ethias)",
            }

            return (
                f"<li>Periode: {insurance.start_date.strftime('%d %b %Y %H:%M')} - {insurance.end_date.strftime('%d %b %Y %H:%M')}</li>"
                f"<li>Aard van activiteit: {insurance.nature}</li>"
                f"<li>Land: België</li>"
                + city
                + f"<li>Grootte van evenement:  {event_sizes[insurance.event_size]}</li>"
                f"<li>Opmerkingen: {insurance.comment if insurance.comment else 'geen'}</li>"
            )
        elif isinstance(insurance, ActivityInsurance):
            city = f"<li>Locatie: {insurance.city}</li>" if insurance.city else ""

            return (
                f"<li>Periode: {insurance.start_date.strftime('%d %b %Y')} - {insurance.end_date.strftime('%d %b %Y')}</li>"
                f"<li>Aard van activiteit: {insurance.nature}</li>"
                f"<li>Land: België</li>"
                + city
                + f"<li>Aantal extra te verzekeren personen:  {GroupSize.from_choice(insurance.group_size)[1]}</li>"
                f"<li>Opmerkingen: {insurance.comment if insurance.comment else 'geen'}</li>"
            )
        elif isinstance(insurance, TravelAssistanceInsurance):
            participants = list()
            for participant in insurance.participants.all():
                participants.append(participant.full_name())
            vehicle = (
                f"<li>Voertuig: {insurance.vehicle_with_simple_trailer_to_str_mail()}</li>"
                if insurance.vehicle
                else ""
            )
            return (
                f"<li>Periode: {insurance.start_date.strftime('%d %b %Y')} - {insurance.end_date.strftime('%d %b %Y')}</li>"
                f"<li>Land: {insurance.country if insurance.country else 'België'}</li>"
                f"<li>Deelnemers: {', '.join(participants)}</li>"
                + vehicle
                + f"<li>Opmerkingen: {insurance.comment if insurance.comment else 'geen'}</li>"
            )
        return ""

    def _extra_text(self, insurance: BaseInsurance) -> str:
        # frontend_base_url = settings.FRONTEND_BASE_URL #USE THIS ENV VAR FOR LOCAL
        frontend_base_url = settings.BASE_URL  # USE THIS ENV VAR FOR ACC AND PROD
        if (insurance.type.description.lower() == "eenmalige activiteit") or (
            insurance.type.description.lower() == "evenementen verzekering"
        ):
            return f"<div>&nbsp;</div>Vergeet niet om na de activiteit <a style='text-decoration: underline;' href='https://www.scoutsengidsenvlaanderen.be/media/1317/download'>de deelnemerslijst</a> in te vullen en te bezorgen, ook als er geen ongeval gebeurde. Je kan het in <a style='text-decoration: underline;' href='{frontend_base_url}/#/eenmalige-activiteit-detail/{insurance.id}'>je aanvraag</a> opladen.<div>&nbsp;</div>"

        if insurance.type.description.lower() == "autoverzekering":
            # return f"<div>&nbsp;</div>Voor eigen voertuigen kan Ethias deze aanvraag pas goedkeuren na ontvangst van het ingevulde expertiseverslag. Voor gehuurde voertuigen kan Scouts en Gidsen Vlaanderen deze aanvraag pas goedkeuren na ontvangst van het huurcontract met beschrijving van de staat van het voertuig. Je kan het in <a style='text-decoration: underline;' href='{frontend_base_url}/#/eenmalige-activiteit-detail/{insurance.id}'>je aanvraag</a> opladen.<div>&nbsp;</div>"
            return f"<div>&nbsp;</div>Ten vroegste 2 werkdagen en minimum 1 werkdag voor je op scoutsactiviteit vertrekt moet je online het <a style='text-decoration: underline;' href='https://forms.office.com/Pages/ResponsePage.aspx?id=_EiNAphkiESNwUyecUlr-F2-J9LUk9NNsZ0o6D7lSvhUN1pGQ1k5NDNWT1ZCTDFVUDdFT09ZQk9XRSQlQCN0PWcu'>expertiseformulier</a> van Ethias invullen. Meer uitleg over deze procedure vind je <a style='text-decoration: underline;' href='https://www.scoutsengidsenvlaanderen.be/leiding/ondersteuning/groepsleiding/verzekeringen/autoverzekering#expertiseformulier'>op onze website</a>.<div>&nbsp;</div>"

        return "<div>&nbsp;</div>"

    def _prepare_email_body(self, template_path: str, dictionary: dict) -> str:
        return TextUtils.replace(
            path=template_path, dictionary=dictionary, placeholder_start="--", placeholder_end="--"
        )

    def _send_prepared_insurance_email(
        self,
        insurance: BaseInsurance,
        subject: str,
        template_path: str,
        to: list = None,
        cc: list = None,
        bcc: list = settings.EMAIL_INSURANCE_BCC,
        reply_to: str = None,
        template_id: str = None,
        add_attachments: bool = False,
        tags=None,
    ):
        if tags is None:
            tags = []

        if not reply_to:
            reply_to = self.from_email

        values = self._prepare_insurance_dictionary(insurance, settings.USE_SENDINBLUE)

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
            mail.template_id = settings.SENDINBLUE_TEMPLATE_INSURANCE_REQUESTER
            mail.body = json.dumps(values)
        else:
            mail.is_html = True
            html_body = self._prepare_email_body(template_path, values)
            html_body = TextUtils.compose_html_email(
                self.template_path_start,
                html_body,
                self.template_path_end
            )
            # Voorkom dat Brevo automatisch achter elke lijn een '<br>' plakt.
            html_body = " ".join(html_body.splitlines())
            # Combineer opeenvolgende spaties
            mail.html_body = re.sub("  +", " ", html_body)

        self.send(mail, tags=tags)
