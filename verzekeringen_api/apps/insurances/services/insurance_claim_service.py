from datetime import datetime, date

from django.core.exceptions import ValidationError
from django.db import transaction
from pdfrw import PdfReader, PdfDict, PdfObject, PdfName, PdfWriter

from ..models.insurance_claim import InsuranceClaim, InsuranceClaimVictim
import os
from django.conf import settings
from django.core.mail import EmailMessage

from ...mailing.services import sendTemplateEmail
from ...members.services.group_admin_member_service import group_admin_member_detail
from ...members.utils import GroupAdminMember


def _get_temp_file(filename: str):
    return "%s/%s" % (settings.TMP_FOLDER, filename)


@transaction.atomic
def insurance_claim_create(
    *,
    created_by: settings.AUTH_USER_MODEL,
    declarant_city: str = None,
    group_id: str,
    bank_account: str = None,
    date_of_accident: datetime,
    activity: str = None,
    activity_type: str = None,
    location: str = None,
    used_transport: str = None,
    damage_type: str = None,
    description: str = None,
    involved_party_description: str = None,
    involved_party_name: str = None,
    involved_party_birthdate: date = None,
    official_report_description: str = None,
    pv_number: str = None,
    witness_name: str = None,
    witness_description: str = None,
    leadership_description: str = None,
    victim: InsuranceClaimVictim,
) -> InsuranceClaim:
    # validate if person have rights to create claim for this group
    if group_id not in (group.id for group in created_by.partial_scouts_groups):
        raise ValidationError("Given group %s is not a valid group of user" % group_id)

    # Assuming that the group_admin_id has been loaded when adding the victim to the claim
    # @ricardo: check this please
    # if victim.group_admin_id:
    #     victim.get_member_number()
    victim.save()

    claim = InsuranceClaim(
        date=datetime.now(),
        declarant=created_by,
        declarant_city=declarant_city,
        group_number=group_id,
        bank_account=bank_account,
        date_of_accident=date_of_accident,
        activity=activity,
        activity_type=activity_type,
        location=location,
        used_transport=used_transport,
        damage_type=damage_type,
        description=description,
        involved_party_description=involved_party_description,
        involved_party_name=involved_party_name,
        involved_party_birthdate=involved_party_birthdate,
        official_report_description=official_report_description,
        pv_number=pv_number,
        witness_name=witness_name,
        witness_description=witness_description,
        leadership_description=leadership_description,
        victim=victim,
    )

    claim.full_clean()
    claim.save()

    return claim


def send_pdf(claim):
    filename = generate_pdf(claim)

    sendTemplateEmail(
        receivers=[settings.INSURANCE_MAIL],
        template_id=settings.SENDINBLUE_TEMPLATE_ID,
        file=filename,
    )
    os.remove(filename)


def generate_pdf(claim):
    owner: GroupAdminMember = group_admin_member_detail(
        active_user=claim.declarant, group_admin_id=claim.declarant.group_admin_id
    )
    victim = claim.victim
    model = {
        "(Benaming)": claim.group_number,
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
        "(Geslacht_2)": victim.sex,
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
                            AS=PdfName("061_Op_weg_naar_van_activiteit"), V=PdfName("061_Op_weg_naar_van_activiteit")
                        )
                    )
                    property["/Kids"][2].update(
                        PdfDict(
                            AS=PdfName("061_Op_weg_naar_van_activiteit"), V=PdfName("061_Op_weg_naar_van_activiteit")
                        )
                    )

                if activity_type == "OTHER":
                    property.update(PdfDict(AS=PdfName("087_Andere"), V=PdfName("087_Andere")))
                    property["/Kids"][3].update(PdfDict(AS=PdfName("087_Andere"), V=PdfName("087_Andere")))

    filename = _get_temp_file(filename=("verzekeringen-%s.pdf" % claim.id))

    PdfWriter().write(filename, template)
    return filename
