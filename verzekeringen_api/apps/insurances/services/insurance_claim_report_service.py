import logging

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage, FileSystemStorage

from pdfrw import PdfReader, PdfDict, PdfObject, PdfName, PdfWriter

from apps.insurances.models import InsuranceClaim, InsuranceClaimVictim, InsuranceClaimAttachment
from apps.insurances.utils import InsuranceAttachmentUtils
from inuits.files import FileUtils
from groupadmin.models import ScoutsMember
from groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class InsuranceClaimReportService:

    store_report = settings.STORE_INSURANCE_CLAIM_REPORT_WHILE_DEBUGGING

    local_storage = FileSystemStorage()
    default_storage = default_storage
    group_admin_service = GroupAdmin()

    def generate_pdf(self, claim: InsuranceClaim):
        owner: ScoutsMember = self.group_admin_service.get_member_info(
            active_user=claim.declarant, group_admin_id=claim.declarant.group_admin_id
        )
        victim: InsuranceClaimVictim = claim.victim
        model = {
            "(Benaming)": claim.group_group_admin_id,
            "(Naam_Verantwoordelijke)": owner.first_name,
            "(Voornnaam_Verantwoordelijke)": owner.last_name,
            "(E-mail)": owner.email,
            "(Naam_Slachtoffer)": victim.first_name,
            "(Voornaam_Slachtoffer)": victim.last_name,
            "(E-mail_Slachtoffer)": victim.email,
            "(Beroep)": victim.legal_representative,
            "(Straat_2)": victim.address.street,
            "(Nr_2)": victim.address.number,
            "(Postcode_2)": str(victim.address.postcode_city.postcode),
            "(Gemeente_2)": victim.address.postcode_city.name,
            "(Bus_2)": victim.address.letter_box,
            "(Land_2)": "België",
            "(Geslacht_2)": victim.gender,
            "(Taal)": "N",
            "(Geboorte_Dag)": f"{victim.birth_date.day:02d}",
            "(Geboorte_Maand)": f"{victim.birth_date.month:02d}",
            "(Geboorte_Jaar)": str(victim.birth_date.year),
            "(Ongeval_Dag)": f"{claim.date_of_accident.date().day:02d}",
            "(Ongeval_Maand)": f"{claim.date_of_accident.date().month:02d}",
            "(Ongeval_Jaar)": str(claim.date_of_accident.date().year),
            "(Lidnummer)": victim.get_member_number(claim.declarant),
            "(IBAN_1)": claim.bank_account[2:4] if claim.bank_account else "",
            "(IBAN_2)": claim.bank_account[4:8] if claim.bank_account else "",
            "(IBAN_3)": claim.bank_account[8:12] if claim.bank_account else "",
            "(IBAN_4)": claim.bank_account[12:16] if claim.bank_account else "",
            "(Beschrijving_Ongeval)": claim.description,
            "(Plaats_Ongeval)": claim.location,
            "(Beoefende_sport/activiteit)": claim.activity,
            "(Andere)": claim.damage_type,
            "(Naam_Andere)": claim.involved_party_name,
            "(Adres_Andere)": claim.involved_party_description,
            "(Welke_autoriteit)": claim.official_report_description,
            "(Gebruikte_Vervoermiddel)": claim.used_transport,
            "(Nr_PV)": claim.pv_number,
            "(Naam_Getuige_1)": claim.witness_name,
            "(Adres_getuige_1)": claim.witness_description,
            "(Toezichthouder)": claim.leadership_description,
            "(Ondertekening_Dag)": f"{claim.date.date().day:02d}",
            "(Ondertekening_Maand)": f"{claim.date.date().month:02d}",
            "(Ondertekening_Jaar)": str(claim.date.date().year),
            "(Plaats_opmaak_1)": claim.declarant_city if claim.declarant_city else owner.address.postcode_city.name,
            "(Identiteit_Aangever)": ("%s %s" % (owner.first_name, owner.last_name)),
        }

        if claim.involved_party_birthdate:
            model["(Geboorte_Dag_2)"] = f"{claim.involved_party_birthdate.day:02d}"
            model["(Geboorte_Maand_2)"] = f"{claim.involved_party_birthdate.month:02d}"
            model["(Geboorte_Jaar_2)"] = str(claim.involved_party_birthdate.year)

        template = PdfReader(settings.PDF_TEMPLATE_PATH)

        template.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject("true")))

        for property in template.Root.AcroForm.Fields:
            if property["/T"] in model:
                if model.get(property["/T"], False):
                    property.update(PdfDict(V=model.get(property["/T"])))

            # For radio buttons, its necessary to change child widget also
            if property["/T"] == "(Geslacht_2)":
                if model.get("(Geslacht_2)") == "M":
                    property.update(PdfDict(AS=PdfName("M"), V=PdfName("M")))
                    property["/Kids"][0].update(PdfDict(AS=PdfName("M"), V=PdfName("M")))
                else:
                    property.update(PdfDict(AS=PdfName("V"), V=PdfName("V")))
                    property["/Kids"][1].update(PdfDict(AS=PdfName("V"), V=PdfName("V")))

            if property["/T"] == "(Taal)":
                if model.get("(Taal)") == "N":
                    property.update(PdfDict(AS=PdfName("N"), V=PdfName("N")))
                    property["/Kids"][0].update(PdfDict(AS=PdfName("N"), V=PdfName("N")))
                else:
                    property.update(PdfDict(AS=PdfName("F"), V=PdfName("F")))
                    property["/Kids"][1].update(PdfDict(AS=PdfName("F"), V=PdfName("F")))

            if property["/T"] == "(Lid)":
                property.update(PdfDict(AS=PdfName("Lid"), V=PdfName("Lid")))
                property["/Kids"][0].update(PdfDict(AS=PdfName("Lid"), V=PdfName("Lid")))

            if property["/T"] == "(Fout_Derde)":
                if claim.involved_party_description:
                    property.update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                    property["/Kids"][0].update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                else:
                    property.update(PdfDict(AS=PdfName("Neen"), V=PdfName("Neen")))
                    property["/Kids"][1].update(PdfDict(AS=PdfName("Neen"), V=PdfName("Neen")))

            if property["/T"] == "(Vaststelling)":
                if claim.official_report_description or claim.pv_number:
                    property.update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                    property["/Kids"][0].update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                else:
                    property.update(PdfDict(AS=PdfName("Neen"), V=PdfName("Neen")))
                    property["/Kids"][1].update(PdfDict(AS=PdfName("Neen"), V=PdfName("Neen")))

            if property["/T"] == "(Getuigen)":
                if claim.witness_description or claim.witness_name:
                    property.update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                    property["/Kids"][0].update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                else:
                    property.update(PdfDict(AS=PdfName("Neen"), V=PdfName("Neen")))
                    property["/Kids"][1].update(PdfDict(AS=PdfName("Neen"), V=PdfName("Neen")))

            if property["/T"] == "(Toezicht)":
                if claim.leadership_description:
                    property.update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                    property["/Kids"][0].update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                else:
                    property.update(PdfDict(AS=PdfName("Neen"), V=PdfName("Neen")))
                    property["/Kids"][1].update(PdfDict(AS=PdfName("Neen"), V=PdfName("Neen")))

            if property["/T"] == "(Code_activiteit)":
                for activity_type in claim.activity_type:
                    if activity_type == "REGULAR":
                        property.update(PdfDict(AS=PdfName("400_Training_club"), V=PdfName("400_Training_club")))
                        property["/Kids"][0].update(
                            PdfDict(AS=PdfName("400_Training_club"), V=PdfName("400_Training_club"))
                        )

                    if activity_type == "IRREGULAR_LOCATION":
                        property.update(
                            PdfDict(AS=PdfName("420_Training_individueel"), V=PdfName("420_Training_individueel"))
                        )
                        property["/Kids"][1].update(
                            PdfDict(AS=PdfName("420_Training_individueel"), V=PdfName("420_Training_individueel"))
                        )

                    if activity_type == "TRANSPORT":
                        property.update(
                            PdfDict(
                                AS=PdfName("061_Op_weg_naar_van_activiteit"),
                                V=PdfName("061_Op_weg_naar_van_activiteit"),
                            )
                        )
                        property["/Kids"][2].update(
                            PdfDict(
                                AS=PdfName("061_Op_weg_naar_van_activiteit"),
                                V=PdfName("061_Op_weg_naar_van_activiteit"),
                            )
                        )

                    if activity_type == "OTHER":
                        property.update(PdfDict(AS=PdfName("087_Andere"), V=PdfName("087_Andere")))
                        property["/Kids"][3].update(PdfDict(AS=PdfName("087_Andere"), V=PdfName("087_Andere")))

        report_filename = InsuranceAttachmentUtils.generate_claim_report_temp_file_name(claim)
        filename = FileUtils.get_temp_file(filename=report_filename)
        logger.debug("Generating pdf report for claim(%d) and saving it to %s", claim.id, filename)

        PdfWriter().write(filename, template)

        if self.store_report:
            report_filename = InsuranceAttachmentUtils.get_claim_base_path() + report_filename
            logger.debug(
                "STORE_INSURANCE_CLAIM_REPORT_WHILE_DEBUGGING is set to True, saving the report (%s) with default_storage to %s",
                filename,
                report_filename,
            )

            with open(filename, "rb") as f:
                self.default_storage.save(report_filename, ContentFile(f.read()))

        return filename
