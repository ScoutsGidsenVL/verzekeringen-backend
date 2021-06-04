from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_yasg2.utils import swagger_auto_schema
from ...models import Country
from ..serializers import CountryOutputSerializer


class CountryByInsuranceTypeView(views.APIView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: CountryOutputSerializer})
    def get(self, request, **kwargs):
        type_id = kwargs.get("type_id")

        countries = Country.objects.by_type(type_id)
        output_serializer = CountryOutputSerializer(countries, many=True)

        return Response(output_serializer.data)
