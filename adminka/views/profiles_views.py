from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from adminka.permissions import IsOrganizerOrSupervisor
from adminka.serializers import *
from crm.models import *


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