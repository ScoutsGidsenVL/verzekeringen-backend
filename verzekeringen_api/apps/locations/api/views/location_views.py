from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_yasg2.utils import swagger_auto_schema
from ..serializers import BelgianPostcodeCityOutputSerializer
from ...services import LocationService


class BelgianPostcodeCitySearch(views.APIView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: BelgianPostcodeCityOutputSerializer})
    def get(self, request):
        search_term = self.request.GET.get("term", None)
        if not search_term:
            raise ValidationError("Url param 'term' is a required filter")
        results = LocationService.belgian_postcode_city_search(term=search_term)
        output_serializer = BelgianPostcodeCityOutputSerializer(results, many=True)

        return Response(output_serializer.data)
