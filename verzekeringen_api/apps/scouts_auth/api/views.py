from rest_framework import views, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from .serializers import UserDetailOutputSerializer


class CurrentUserView(views.APIView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: UserDetailOutputSerializer})
    def get(self, request):
        request.user.fetch_detailed_group_info()
        output_serializer = UserDetailOutputSerializer(request.user)

        return Response(output_serializer.data)
