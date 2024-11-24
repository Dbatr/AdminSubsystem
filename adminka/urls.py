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

    path('efficiencies/', get_all_efficiencies, name='get_all_efficiencies'),
    path('efficiency/<int:user_id>/', get_efficiency_by_user, name='get_efficiency_by_user'),
    path('efficiency/create/', create_efficiency, name='create_efficiency'),
    path('efficiency/<int:user_id>/update/', update_efficiency, name='update_efficiency'),
    path('efficiency/<int:user_id>/partial/', partial_update_efficiency, name='partial_update_efficiency'),
    path('efficiency/<int:user_id>/delete/', delete_efficiency, name='delete_efficiency'),
]