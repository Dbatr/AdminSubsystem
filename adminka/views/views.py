from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from adminka.permissions import IsOrganizerOrSupervisor


# Role check
class SomeProtectedView(APIView):
    permission_classes = [IsOrganizerOrSupervisor]

    @extend_schema(
        responses={200: 'Доступ разрешен!'},
        description="Пример проверки роли пользователя."
    )
    def get(self, request):
        return Response({"message": "Доступ разрешен!"})










