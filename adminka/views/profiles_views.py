from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from adminka.permissions import *
from adminka.serializers import *
from crm.models import *


class AllProfilesView(APIView):
    """
    Получение всех профилей.
    """

    @extend_schema(
        tags=["Profiles"],
        parameters=[
            OpenApiParameter(name='name', type=OpenApiTypes.STR, description='Фильтрация по имени', required=False),
            OpenApiParameter(name='email', type=OpenApiTypes.STR, description='Фильтрация по email', required=False),
            OpenApiParameter(name='university', type=OpenApiTypes.STR, description='Фильтрация по университету',
                             required=False),
            OpenApiParameter(name='telegram', type=OpenApiTypes.STR, description='Фильтрация по Telegram',
                             required=False),
            OpenApiParameter(name='surname', type=OpenApiTypes.STR, description='Фильтрация по фамилии',
                             required=False),
            OpenApiParameter(name='patronymic', type=OpenApiTypes.STR, description='Фильтрация по отчеству',
                             required=False),
            OpenApiParameter(name='course', type=OpenApiTypes.STR, description='Фильтрация по курсу', required=False),
            OpenApiParameter(name='skills', type=OpenApiTypes.STR, description='Фильтрация по навыкам', required=False),
        ],
        responses=ProfileSerializer(many=True),
        description="Получение списка всех профилей. Можно фильтровать по полям, передавая параметры в запросе."
    )
    def get(self, request):

        filter_params = {key: value for key, value in request.query_params.items() if value}

        profiles = Profile.objects.all()

        if filter_params:
            profiles = profiles.filter(**filter_params)

        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileDetailView(APIView):
    permission_classes = [IsOrganizerOrSupervisor]  # Потребуется аутентификация

    @extend_schema(
        tags=["Profiles"],
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
    permission_classes = [IsOrganisatorOrSupervisor]
    @extend_schema(
        tags=["Profiles"],
        request=ProfileSerializer_post_put_patch,
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
                return Response({"detail": "У данного пользователя уже есть профиль."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Создаем профиль для пользователя
            serializer = ProfileSerializer_post_put_patch(data=request.data)
            if serializer.is_valid():
                # Указываем автора профиля из user_id
                serializer.save(author=user)
                return Response({"message": "Профиль успешно создан.", "data": serializer.data},
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        tags=["Profiles"],
        request=ProfileSerializer_post_put_patch,
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
            serializer = ProfileSerializer_post_put_patch(profile, data=request.data)
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
        tags=["Profiles"],
        request=ProfileSerializer_post_put_patch(partial=True),
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
            serializer = ProfileSerializer_post_put_patch(profile, data=request.data, partial=True)
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


class RoleByTokenView(APIView):
    """
    Получение роли пользователя по токену.
    """
    permission_classes = [IsOrganizerOrSupervisor]

    @extend_schema(
        tags=["Roles"],
        responses={200: RoleSerializer(many=True), 404: 'Роль не найдена.'},
        description="Получение роли пользователя по токену."
    )
    def get(self, request):
        try:
            # Получаем профиль текущего пользователя
            profile = request.user.profile

            # Получаем связанные роли
            roles = profile.users.all()
            if not roles:
                return Response({"detail": "Роли не найдены."}, status=status.HTTP_404_NOT_FOUND)

            # Сериализуем роли
            serializer = RoleSerializer(roles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AttributeError:
            return Response({"detail": "У пользователя нет профиля."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)