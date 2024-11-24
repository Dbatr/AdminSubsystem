from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from adminka.permissions import IsOrganizerOrSupervisor
from adminka.serializers import *
from crm.models import *
from django.shortcuts import get_object_or_404


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


class AllProfilesView(APIView):
    """
    Получение всех профилей.
    """

    @extend_schema(
        responses=ProfileSerializer(many=True),
        description="Получение списка всех профилей."
    )
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllUsersView(APIView):
    """
    Получение всех пользователей.
    """

    @extend_schema(
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
        responses={200: UserSerializer, 404: 'Пользователь не найден.'},
        description="Получение данных пользователя по ID."
    )
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Role check
class SomeProtectedView(APIView):
    permission_classes = [IsOrganizerOrSupervisor]

    @extend_schema(
        responses={200: 'Доступ разрешен!'},
        description="Пример проверки роли пользователя."
    )
    def get(self, request):
        return Response({"message": "Доступ разрешен!"})


class ProfileDetailView(APIView):
    permission_classes = [IsOrganizerOrSupervisor]  # Потребуется аутентификация

    @extend_schema(
        parameters=[int],
        responses={200: ProfileSerializer, 404: 'Профиль не найден.'},
        description="Получение профиля по ID."
    )
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


class AdminProfileView(APIView):
    """
    API для создания, полного и частичного обновления профиля пользователя.
    """

    @extend_schema(
        request=ProfileSerializer,
        responses={201: ProfileSerializer, 400: 'Ошибка валидации', 404: 'Пользователь не найден.'},
        description="Создание профиля для пользователя."
    )
    def post(self, request, user_id):
        """
        Создание профиля для указанного пользователя.
        """
        try:
            # Получаем пользователя по ID
            user = User.objects.get(id=user_id)

            # Проверяем, существует ли уже профиль
            if hasattr(user, 'profile'):
                return Response({"detail": "У данного пользователя уже есть профиль."}, status=status.HTTP_400_BAD_REQUEST)

            # Создаем профиль для пользователя
            data = request.data
            data['author'] = user.id  # Привязываем профиль к указанному пользователю
            serializer = ProfileSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Профиль успешно создан.", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        request=ProfileSerializer,
        responses={200: ProfileSerializer, 404: 'Профиль не найден.'},
        description="Полное обновление профиля."
    )
    def put(self, request, user_id):
        """
        Полное обновление профиля указанного пользователя.
        """
        try:
            # Получаем пользователя и профиль
            user = User.objects.get(id=user_id)
            profile = user.profile

            # Полное обновление профиля
            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Профиль успешно обновлен.", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

        except Profile.DoesNotExist:
            return Response({"detail": "Профиль не найден."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        request=ProfileSerializer(partial=True),
        responses={200: ProfileSerializer, 404: 'Профиль не найден.'},
        description="Частичное обновление профиля."
    )
    def patch(self, request, user_id):
        """
        Частичное обновление профиля указанного пользователя.
        """
        try:
            # Получаем пользователя и профиль
            user = User.objects.get(id=user_id)
            profile = user.profile

            # Частичное обновление профиля
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Профиль успешно обновлен.", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

        except Profile.DoesNotExist:
            return Response({"detail": "Профиль не найден."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Получение всех навыков
@extend_schema(
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
    request=SkillSerializer,
    responses={201: SkillSerializer, 400: 'Ошибка валидации'},
    description="Добавление нового навыка."
)
@api_view(['POST'])
def add_skill(request):
    if request.method == 'POST':
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Удаление навыка
@extend_schema(
    parameters=[int],
    responses={204: None, 404: 'Навык не найден.'},
    description="Удаление навыка."
)
@api_view(['DELETE'])
def delete_skill(request, pk):
    try:
        skill = Skill.objects.get(pk=pk)
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Skill.DoesNotExist:
        return Response({"detail": "Навык не найден."}, status=status.HTTP_404_NOT_FOUND)