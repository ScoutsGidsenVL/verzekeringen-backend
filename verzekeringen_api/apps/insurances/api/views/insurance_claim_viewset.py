import os
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.members.models import InuitsNonMember
from apps.members.services.group_admin_member_service import group_admin_member_detail
from apps.members.utils import GroupAdminMember
from ..serializers import (
    BaseInsuranceClaimSerializer,
    InsuranceClaimInputSerializer, InsuranceClaimDetailOutputSerializer
)
from ...models.insurance_claim import InsuranceClaim
from ...services import InsuranceClaimService
from pdfrw import PdfReader, PdfDict, PdfWriter, PdfName, PdfObject

class InsuranceClaimViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["date"]
    ordering = ["-date"]

    def _get_temp_file(self, filename):
        return '%s/%s' % (settings.TMP_FOLDER, filename)

    def get_queryset(self):
        return InsuranceClaim.objects.all()

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceClaimDetailOutputSerializer})
    def retrieve(self, request, pk=None):
        claim = self.get_object()
        serializer = InsuranceClaimDetailOutputSerializer(claim, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: BaseInsuranceClaimSerializer})
    def list(self, request):
        insurances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(insurances)

        if page is not None:
            serializer = BaseInsuranceClaimSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        else:
            serializer = BaseInsuranceClaimSerializer(insurances, many=True, context={"request": request})
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InsuranceClaimInputSerializer,
        responses={status.HTTP_201_CREATED: InsuranceClaimDetailOutputSerializer},
    )
    def create(self, request):
        input_serializer = InsuranceClaimInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        claim: InsuranceClaim = InsuranceClaimService.insurance_claim_create(created_by=request.user,
                                                                             **input_serializer.validated_data)
        owner: GroupAdminMember = group_admin_member_detail(active_user=claim.declarant, group_admin_id=request.user.group_admin_id)
        victim = claim.get_victim()

        if not isinstance(victim, InuitsNonMember):
            victim = group_admin_member_detail(active_user=request.user, group_admin_id=victim)
        else:
            victim.birth_date = claim.victim_birth_date
            victim.email = None
            victim.membership_number = "NO LIDNUMMER"

        model = {
            '(Benaming)': claim.group_number,
            '(Beroep)': claim.legal_representative,
            '(Beschrijving_Ongeval)': claim.description,
            '(Naam_Verantwoordelijke)': owner.first_name,
            '(Voornnaam_Verantwoordelijke)': owner.last_name,
            '(E-mail)': owner.email,
            '(Naam_Slachtoffer)': victim.first_name,
            '(Voornaam_Slachtoffer)': victim.last_name,
            '(Straat_2)': victim.address.street,
            '(Nr_2)': victim.address.number,
            '(Postcode_2)': victim.address.postcode_city.postcode,
            '(Gemeente_2)': victim.address.postcode_city.name,
            '(Bus_2)': victim.address.letter_box,
            '(Land_2)': 'België',
            '(Geslacht_2)': claim.sex,
            # '(Taal)': 'N',
            '(Geboorte_Dag)': f'{victim.birth_date.day:02d}',
            '(Geboorte_Maand)': f'{victim.birth_date.month:02d}',
            '(Geboorte_Jaar)': str(victim.birth_date.year),
            '(Ongeval_Dag)': f'{claim.date_of_accident.date().day:02d}',
            '(Ongeval_Maand)': f'{claim.date_of_accident.date().month:02d}',
            '(Uur_ongeval_1)': ('%s %s' % (claim.date_of_accident.time().hour, claim.date_of_accident.time().minute)),
            '(Ongeval_Jaar)': str(claim.date_of_accident.date().year),
            '(E-mail_Slachtoffer)': victim.email,
            '(Lidnummer)': victim.membership_number,
            '(IBAN_1)': claim.bank_account[2:4] if claim.bank_account else '',
            '(IBAN_2)': claim.bank_account[4:8] if claim.bank_account else '',
            '(IBAN_3)': claim.bank_account[8:12] if claim.bank_account else '',
            '(IBAN_4)': claim.bank_account[12:16] if claim.bank_account else '',
            '(Beoefende_sport/activiteit)': claim.activity,
            '(Naam_Andere)': claim.involved_party_description,
            '(Welke_autoriteit)': claim.official_report_description,
            '(Gebruikte_Vervoermiddel)': claim.used_transport,
            '(Nr_PV)': claim.pv_number,
            '(Naam_Getuige_1)': claim.witness_name,
            '(Adres_getuige_1)': claim.witness_description,
            '(Toezichthouder)': claim.leadership_description,
            '(Ondertekening_Dag)': f'{claim.date.date().day:02d}',
            '(Ondertekening_Maand)': f'{claim.date.date().month:02d}',
            '(Ondertekening_Jaar)': str(claim.date.date().year),
            '(Plaats_opmaak_1)': claim.declarant_city if not claim.declarant_city else owner.address.postcode_city.name,
            '(Identiteit_Aangever)': ('%s %s' % (owner.first_name, owner.last_name))
        }

        if claim.involved_party_birthdate:
            model['(Geboorte_Dag_2)'] = f'{claim.involved_party_birthdate.day:02d}'
            model['(Geboorte_Maand_2)'] = f'{claim.involved_party_birthdate.month:02d}'
            model['(Geboorte_Jaar_2)'] = str(claim.involved_party_birthdate.year)

        template = PdfReader(settings.PDF_TEMPLATE_PATH)

        template.Root.AcroForm.update(PdfDict(NeedAppearances=PdfObject('true')))

        for property in template.Root.AcroForm.Fields:
            if property['/T'] in model:
                if model.get(property['/T'], False):
                    # https://stackoverflow.com/questions/54279950/how-to-edit-editable-pdf-using-the-pdfrw-library
                    property.update(
                        PdfDict(V=model.get(property['/T']))
                    )

            if property['/T'] == '(Geslacht_2)':
                if model.get('(Geslacht_2)') == 'M':
                    property.update(PdfDict(AS=PdfName('M'), V=PdfName('M')))
                    property['/Kids'][0].update(PdfDict(AS=PdfName('M'), V=PdfName('M')))
                else:
                    property.update(PdfDict(AS=PdfName('V'), V=PdfName('V')))
                    property['/Kids'][1].update(PdfDict(AS=PdfName('V'), V=PdfName('V')))

            if property['/T'] == '(Taal)':
                if model.get('(Taal)') == 'N':
                    property.update(PdfDict(AS=PdfName('N'), V=PdfName('N')))
                    property['/Kids'][0].update(PdfDict(AS=PdfName('N'), V=PdfName('N')))
                else:
                    property.update(PdfDict(AS=PdfName('F'), V=PdfName('F')))
                    property['/Kids'][1].update(PdfDict(AS=PdfName('F'), V=PdfName('F')))

            if property['/T'] == '(Lid)':
                property['/Kids'][0].update(PdfDict(AS=PdfName('Lid'), V=PdfName('Lid')))

            if property['/T'] == '(Fout_Derde)':
                if claim.involved_party_description:
                    property.update(PdfDict(AS=PdfName('Ja'), V=PdfName('Ja')))
                    property['/Kids'][0].update(PdfDict(AS=PdfName('Ja'), V=PdfName('Ja')))
                else:
                    property.update(PdfDict(AS=PdfName('Neen'), V=PdfName('Neen')))
                    property['/Kids'][1].update(PdfDict(AS=PdfName('Neen'), V=PdfName('Neen')))

            if property['/T'] == '(Vaststelling)':
                if claim.involved_party_description:
                    property.update(PdfDict(AS=PdfName('Ja'), V=PdfName('Ja')))
                    property['/Kids'][0].update(PdfDict(AS=PdfName('Ja'), V=PdfName('Ja')))
                else:
                    property.update(PdfDict(AS=PdfName('Neen'), V=PdfName('Neen')))
                    property['/Kids'][1].update(PdfDict(AS=PdfName('Neen'), V=PdfName('Neen')))

            if property['/T'] == '(Getuigen)':
                if claim.witness_description:
                    property.update(PdfDict(AS=PdfName('Ja'), V=PdfName('Ja')))
                    property['/Kids'][0].update(PdfDict(AS=PdfName('Ja'), V=PdfName('Ja')))
                else:
                    property.update(PdfDict(AS=PdfName('Neen'), V=PdfName('Neen')))
                    property['/Kids'][1].update(PdfDict(AS=PdfName('Neen'), V=PdfName('Neen')))

            if property['/T'] == '(Toezicht)':
                if claim.leadership_description:
                    property.update(PdfDict(AS=PdfName('Ja'), V=PdfName('Ja')))
                    property['/Kids'][0].update(PdfDict(AS=PdfName('Ja'), V=PdfName('Ja')))
                else:
                    property.update(PdfDict(AS=PdfName('Neen'), V=PdfName('Neen')))
                    property['/Kids'][1].update(PdfDict(AS=PdfName('Neen'), V=PdfName('Neen')))

            if property['/T'] == '(Code_activiteit)':
                if claim.activity_type[0] == 'REGULAR':
                    property.update(PdfDict(AS=PdfName('400_Training_club'), V=PdfName('400_Training_club')))
                    property['/Kids'][0].update(PdfDict(AS=PdfName('400_Training_club'), V=PdfName('400_Training_club')))

                if claim.activity_type[0] == 'IRREGULAR_LOCATION':
                    property.update(PdfDict(AS=PdfName('420_Training_individueel'), V=PdfName('420_Training_individueel')))
                    property['/Kids'][1].update(PdfDict(AS=PdfName('420_Training_individueel'), V=PdfName('420_Training_individueel')))

                if claim.activity_type[0] == 'TRANSPORT':
                    property.update(PdfDict(AS=PdfName('061_Op_weg_naar_van_activiteit'), V=PdfName('061_Op_weg_naar_van_activiteit')))
                    property['/Kids'][2].update(PdfDict(AS=PdfName('061_Op_weg_naar_van_activiteit'), V=PdfName('061_Op_weg_naar_van_activiteit')))

                if claim.activity_type[0] == 'OTHER':
                    property.update(PdfDict(AS=PdfName('087_Andere'), V=PdfName('087_Andere')))
                    property['/Kids'][3].update(PdfDict(AS=PdfName('087_Andere'), V=PdfName('087_Andere')))

        filename = ('verzekeringen-%s.pdf' % (claim.id))

        PdfWriter().write(self._get_temp_file(filename), template)

        email = EmailMessage(
            subject='Insurance claim',
            body='Body goes here',
            to=[settings.INSURANCE_MAIL],
        )

        email.attach_file(self._get_temp_file(filename))
        email.send()
        os.remove(('%s/%s' % (settings.TMP_FOLDER, filename)))

        output_serializer = InsuranceClaimDetailOutputSerializer(claim,  context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)