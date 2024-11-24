from django.urls import path
from adminka.views import *

urlpatterns = [
    path('protected/', SomeProtectedView.as_view(), name='protected_view'),

    path('users/', AllUsersView.as_view(), name='all_users'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='user_detail'),

    path('profiles/', AllProfilesView.as_view(), name='all_profiles'),

    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),  # Для просмотра профиля текущего пользователя
    path('profile/<int:id>/', ProfileDetailView.as_view(), name='profile_detail_other'),  # Для просмотра профиля по id
    path('profile/create/<int:user_id>/', AdminProfileView.as_view(), name='admin_create_profile'),  # Создание профиля для юзера или обновление

    path('skills/', get_all_skills, name='get_all_skills'),
    path('skills/<int:pk>/', get_skill_by_id, name='get_skill_by_id'),
    path('skills/add/', add_skill, name='add_skill'),
    path('skills/delete/<int:pk>/', delete_skill, name='delete_skill'),
]