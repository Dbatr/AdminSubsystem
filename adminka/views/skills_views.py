from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from adminka.serializers import *
from crm.models import *
from adminka.permissions import *


# Получение всех навыков
@extend_schema(
    tags=["Skills"],
    responses=SkillSerializer(many=True),
    description="Получение всех навыков."
)
@api_view(['GET'])
def get_all_skills(request):
    skills = Skill.objects.all()
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)


# Получение навыка по ID
@extend_schema(
    tags=["Skills"],
    parameters=[int],
    responses={200: SkillSerializer, 404: 'Навык не найден.'},
    description="Получение навыка по ID."
)
@api_view(['GET'])
def get_skill_by_id(request, pk):
    try:
        skill = Skill.objects.get(pk=pk)
        serializer = SkillSerializer(skill)
        return Response(serializer.data)
    except Skill.DoesNotExist:
        return Response({"detail": "Навык не найден."}, status=status.HTTP_404_NOT_FOUND)


# Добавление нового навыка
@extend_schema(
    tags=["Skills"],
    request=SkillSerializer,
    responses={201: SkillSerializer, 400: 'Ошибка валидации'},
    description="Добавление нового навыка."
)
@api_view(['POST'])
@permission_classes([IsOrganisatorOrSupervisor])
def add_skill(request):
    if request.method == 'POST':
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Удаление навыка
@extend_schema(
    tags=["Skills"],
    parameters=[int],
    responses={204: None, 404: 'Навык не найден.'},
    description="Удаление навыка."
)
@api_view(['DELETE'])
@permission_classes([IsOrganisatorOrSupervisor])
def delete_skill(request, pk):
    try:
        skill = Skill.objects.get(pk=pk)
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Skill.DoesNotExist:
        return Response({"detail": "Навык не найден."}, status=status.HTTP_404_NOT_FOUND)