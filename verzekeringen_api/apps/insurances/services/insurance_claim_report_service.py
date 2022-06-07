import logging

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage, FileSystemStorage

from pdfrw import PdfReader, PdfDict, PdfObject, PdfName, PdfWriter

from apps.people.models import InuitsClaimVictim
from apps.insurances.models import InsuranceClaim
from apps.insurances.utils import InsuranceAttachmentUtils

from scouts_auth.groupadmin.models import AbstractScoutsMember, AbstractScoutsGroup
from scouts_auth.groupadmin.services import GroupAdmin

from scouts_auth.inuits.files import FileUtils

logger = logging.getLogger(__name__)


class InsuranceClaimReportService:
    store_report = settings.STORE_INSURANCE_CLAIM_REPORT_WHILE_DEBUGGING

    local_storage = FileSystemStorage()
    default_storage = default_storage
    group_admin_service = GroupAdmin()

    def generate_pdf(self, claim: InsuranceClaim):
        declarant_member: AbstractScoutsMember = claim.declarant_member
        victim: InuitsClaimVictim = claim.victim

        logger.debug("DECLARANT MEMBER: %s %s", declarant_member.first_name, declarant_member.last_name)

        model = {
            "(Benaming)": claim.group.full_name,
            "(Naam_Verantwoordelijke)": declarant_member.last_name,
            "(Voornnaam_Verantwoordelijke)": declarant_member.first_name,
            "(E-mail)": declarant_member.email,
            "(Naam_Slachtoffer)": victim.last_name,
            "(Voornaam_Slachtoffer)": victim.first_name,
            "(E-mail_Slachtoffer)": victim.email,
            "(Beroep)": victim.legal_representative,
            "(Straat_2)": victim.street,
            "(Nr_2)": victim.number,
            "(Postcode_2)": str(victim.postal_code),
            "(Gemeente_2)": victim.city,
            "(Bus_2)": victim.letter_box,
            "(Land_2)": "België",
            "(Geslacht_2)": victim.gender,
            "(Taal)": "N",
            "(Geboorte_Dag)": f"{victim.birth_date.day:02d}",
            "(Geboorte_Maand)": f"{victim.birth_date.month:02d}",
            "(Geboorte_Jaar)": str(victim.birth_date.year),
            "(Ongeval_Dag)": f"{claim.date_of_accident.date().day:02d}",
            "(Ongeval_Maand)": f"{claim.date_of_accident.date().month:02d}",
            "(Ongeval_Jaar)": str(claim.date_of_accident.date().year),
            "(Lidnummer)": victim.membership_number,
            "(IBAN_1)": claim.bank_account[2:4] if claim.bank_account else "",
            "(IBAN_2)": claim.bank_account[4:8] if claim.bank_account else "",
            "(IBAN_3)": claim.bank_account[8:12] if claim.bank_account else "",
            "(IBAN_4)": claim.bank_account[12:16] if claim.bank_account else "",
            "(Beschrijving_Ongeval)": claim.description,
            "(Plaats_Ongeval)": claim.location,
            "(Beoefende_sport/activiteit)": claim.activity,
            "(Andere)": claim.damage_type,
            "(Naam_Andere)": claim.involved_party_name if claim.has_involved_party() else "",
            "(Adres_Andere)": claim.involved_party_description if claim.has_involved_party() else "",
            "(Welke_autoriteit)": claim.official_report_description if claim.has_official_report() else "",
            "(Gebruikte_Vervoermiddel)": claim.used_transport,
            "(Nr_PV)": claim.pv_number if claim.has_official_report() else "",
            "(Naam_Getuige_1)": claim.witness_name if claim.has_witness() else "",
            "(Adres_getuige_1)": claim.witness_description if claim.has_witness() else "",
            "(Toezichthouder)": claim.leadership_description if claim.has_leadership() else "",
            "(Ondertekening_Dag)": f"{claim.created_on.date().day:02d}",
            "(Ondertekening_Maand)": f"{claim.created_on.date().month:02d}",
            "(Ondertekening_Jaar)": str(claim.created_on.date().year),
            "(Plaats_opmaak_1)": claim.declarant_city if claim.declarant_city else declarant_member.address.city,
            "(Identiteit_Aangever)": ("%s %s" % (declarant_member.first_name, declarant_member.last_name)),
        }

        if claim.has_involved_party() and claim.involved_party_birthdate:
            model["(Geboorte_Dag_2)"] = f"{claim.involved_party_birthdate.day:02d}"
            model["(Geboorte_Maand_2)"] = f"{claim.involved_party_birthdate.month:02d}"
            model["(Geboorte_Jaar_2)"] = str(claim.involved_party_birthdate.year)

        template = PdfReader(settings.PDF_TEMPLATE_PATH)

        template.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject("true")))

        # TO DEBUG THE PDF
        #
        # for page in template.pages:
        #     annotations = page["/Annots"]

        #     if annotations is None:
        #         continue

        #     for annotation in annotations:
        #         if annotation["/T"]:
        #             logger.debug(annotation["/T"])

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
                if claim.has_involved_party() is not None:
                    if claim.has_involved_party():
                        property.update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                        property["/Kids"][0].update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                    else:
                        property.update(PdfDict(AS=PdfName("Nee"), V=PdfName("Nee")))
                        property["/Kids"][0].update(PdfDict(AS=PdfName("Nee"), V=PdfName("Nee")))

            if property["/T"] == "(Vaststelling)":
                if claim.has_official_report() is not None:
                    if claim.has_official_report():
                        property.update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                        property["/Kids"][0].update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                    else:
                        property.update(PdfDict(AS=PdfName("Nee"), V=PdfName("Nee")))
                        property["/Kids"][0].update(PdfDict(AS=PdfName("Nee"), V=PdfName("Nee")))

            if property["/T"] == "(Getuigen)":
                if claim.has_witness() is not None:
                    if claim.has_witness():
                        property.update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                        property["/Kids"][0].update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                    else:
                        property.update(PdfDict(AS=PdfName("Nee"), V=PdfName("Nee")))
                        property["/Kids"][0].update(PdfDict(AS=PdfName("Nee"), V=PdfName("Nee")))

            if property["/T"] == "(Toezicht)":
                if claim.has_leadership() is not None:
                    if claim.has_leadership():
                        property.update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                        property["/Kids"][0].update(PdfDict(AS=PdfName("Ja"), V=PdfName("Ja")))
                    else:
                        property.update(PdfDict(AS=PdfName("Nee"), V=PdfName("Nee")))
                        property["/Kids"][0].update(PdfDict(AS=PdfName("Nee"), V=PdfName("Nee")))

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
