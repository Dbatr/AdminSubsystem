from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from adminka.permissions import IsOrganizerOrSupervisor
from adminka.serializers import ProfileSerializer, SkillSerializer
from crm.models import *


class SomeProtectedView(APIView):
    permission_classes = [IsOrganizerOrSupervisor]

    def get(self, request):
        return Response({"message": "Доступ разрешен!"})


class ProfileDetailView(APIView):
    permission_classes = [IsOrganizerOrSupervisor]  # Потребуется аутентификация

    def get(self, request, *args, **kwargs):
        profile_id = kwargs.get('id')  # Получаем id из URL

        if profile_id:  # Если в URL передан параметр id
            try:
                # Если указывается id, показываем профиль другого пользователя
                profile = Profile.objects.get(author_id=profile_id)
                serializer = ProfileSerializer(profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Profile.DoesNotExist:
                return Response({"detail": "Профиль не найден."}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                # Если id не передан, показываем профиль текущего пользователя
                profile = request.user.profile
                serializer = ProfileSerializer(profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Profile.DoesNotExist:
                return Response({"detail": "Профиль не найден."}, status=status.HTTP_404_NOT_FOUND)


# Получение всех навыков
@api_view(['GET'])
def get_all_skills(request):
    skills = Skill.objects.all()
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)


# Получение навыка по ID
@api_view(['GET'])
def get_skill_by_id(request, pk):
    try:
        skill = Skill.objects.get(pk=pk)
        serializer = SkillSerializer(skill)
        return Response(serializer.data)
    except Skill.DoesNotExist:
        return Response({"detail": "Навык не найден."}, status=status.HTTP_404_NOT_FOUND)


# Добавление нового навыка
@api_view(['POST'])
def add_skill(request):
    if request.method == 'POST':
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Удаление навыка
@api_view(['DELETE'])
def delete_skill(request, pk):
    try:
        skill = Skill.objects.get(pk=pk)
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Skill.DoesNotExist:
        return Response({"detail": "Навык не найден."}, status=status.HTTP_404_NOT_FOUND)