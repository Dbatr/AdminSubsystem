from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from adminka.serializers import *
from crm.models import *
from django.shortcuts import get_object_or_404


class AllUsersView(APIView):
    """
    Получение всех пользователей.
    """

    @extend_schema(
        tags=["Users"],
        responses=UserSerializer(many=True),
        description="Получение списка всех пользователей."
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    """
    Получение пользователя по ID.
    """

    @extend_schema(
        tags=["Users"],
        responses={200: UserSerializer, 404: 'Пользователь не найден.'},
        description="Получение данных пользователя по ID."
    )
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)