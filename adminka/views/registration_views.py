from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from adminka.serializers import *


# Registration
class SimpleRegistrationView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=SimpleRegistrationSerializer,
        responses={201: 'Пользователь успешно зарегистрирован.', 400: 'Ошибки валидации'}
    )
    def post(self, request):
        serializer = SimpleRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Пользователь успешно зарегистрирован."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
