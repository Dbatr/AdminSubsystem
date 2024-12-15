from rest_framework.permissions import BasePermission
from crm.models import Role


class IsOrganizerOrSupervisor(BasePermission):
    """
    Разрешение для проверки, имеет ли пользователь роль Организатор, Руководитель или Куратор.
    """

    def has_permission(self, request, view):
        # Убедимся, что пользователь аутентифицирован
        if not request.user.is_authenticated:
            return False

        # Получаем профиль пользователя
        profile = getattr(request.user, 'profile', None)
        if profile is None:
            return False

        # Проверяем наличие ролей через модель Role
        allowed_roles = ["Организатор", "Руководитель", "Куратор"]
        return Role.objects.filter(name__in=allowed_roles, users=profile).exists()


class IsOrganisatorOrSupervisor(BasePermission):
    """
    Разрешение для проверки, имеет ли пользователь роль Организатор.
    """

    def has_permission(self, request, view):
        # Убедимся, что пользователь аутентифицирован
        if not request.user.is_authenticated:
            return False

        # Получаем профиль пользователя
        profile = getattr(request.user, 'profile', None)
        if profile is None:
            return False

        # Проверяем наличие ролей через модель Role
        allowed_roles = ["Организатор"]
        return Role.objects.filter(name__in=allowed_roles, users=profile).exists()


class IsOrganisator_RukovodOrSupervisor(BasePermission):
    """
    Разрешение для проверки, имеет ли пользователь роль Организатор, Руководитель.
    """

    def has_permission(self, request, view):
        # Убедимся, что пользователь аутентифицирован
        if not request.user.is_authenticated:
            return False

        # Получаем профиль пользователя
        profile = getattr(request.user, 'profile', None)
        if profile is None:
            return False

        # Проверяем наличие ролей через модель Role
        allowed_roles = ["Организатор", "Руководитель"]
        return Role.objects.filter(name__in=allowed_roles, users=profile).exists()


class IsOrganisator_KuratorOrSupervisor(BasePermission):
    """
    Разрешение для проверки, имеет ли пользователь роль Организатор, Куратор.
    """

    def has_permission(self, request, view):
        # Убедимся, что пользователь аутентифицирован
        if not request.user.is_authenticated:
            return False

        # Получаем профиль пользователя
        profile = getattr(request.user, 'profile', None)
        if profile is None:
            return False

        # Проверяем наличие ролей через модель Role
        allowed_roles = ["Организатор", "Куратор"]
        return Role.objects.filter(name__in=allowed_roles, users=profile).exists()