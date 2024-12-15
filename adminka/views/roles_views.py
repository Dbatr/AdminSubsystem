from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from adminka.serializers import *
from canban.models import *
from django.shortcuts import get_object_or_404
from adminka.permissions import *


@extend_schema(
    tags=["Roles"],
    responses={200: RoleSerializer(many=True)},
    description="Получение списка всех ролей."
)
@api_view(['GET'])
def get_all_roles(request):
    """
    Получение всех ролей.
    """
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Roles"],
    responses={200: RoleSerializer, 404: 'Role not found'},
    description="Получение роли по ID."
)
@api_view(['GET'])
def get_role_by_id(request, role_id):
    """
    Получение роли по ID.
    """
    role = get_object_or_404(Role, id=role_id)
    serializer = RoleSerializer(role)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Roles"],
    request=RoleSerializer,
    responses={201: RoleSerializer, 400: 'Invalid data'},
    description="Создание новой роли."
)
@api_view(['POST'])
@permission_classes([IsOrganisatorOrSupervisor])
def create_role(request):
    """
    Создание новой роли.
    """
    serializer = RoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Roles"],
    responses={204: 'No Content', 404: 'Role not found'},
    description="Удаление роли по ID."
)
@api_view(['DELETE'])
@permission_classes([IsOrganisatorOrSupervisor])
def delete_role(request, role_id):
    """
    Удаление роли по ID.
    """
    role = get_object_or_404(Role, id=role_id)
    role.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["Roles"],
    responses={200: dict},
    description="Получение списка допустимых вариантов ролей."
)
@api_view(['GET'])
def get_valid_roles(request):
    """
    Возвращает список допустимых вариантов ролей.
    """
    valid_roles = [choice[0] for choice in Role.ROLE_CHOISES]
    return Response({"valid_roles": valid_roles}, status=status.HTTP_200_OK)


@extend_schema(
    tags=["Roles"],
    request=AssignRoleSerializer,
    responses={200: "Role assigned successfully", 400: "Invalid data"},
    description="Назначение роли пользователю."
)
@api_view(['POST'])
@permission_classes([IsOrganisatorOrSupervisor])
def assign_role_to_user(request):
    """
    Назначение роли пользователю.
    """
    user_id = request.data.get('user_id')
    role_name = request.data.get('role_name')

    if not user_id or not role_name:
        return Response({"error": "Необходимо указать user_id и role_name."}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(Profile, pk=user_id)
    role = get_object_or_404(Role, name=role_name)

    role.users.add(user)

    return Response({"message": f"Роль '{role_name}' успешно назначена пользователю {user}."}, status=status.HTTP_200_OK)