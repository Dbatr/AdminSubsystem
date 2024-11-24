from django.urls import path

from adminka.views.efficiencies_views import *
from adminka.views.profiles_views import *
from adminka.views.projects_views import *
from adminka.views.skills_views import *
from adminka.views.users_views import *
from adminka.views.views import *

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

    path('projects/', get_all_projects, name='get_all_projects'),
    path('project/<int:project_id>/', get_project_by_id, name='get_project_by_id'),
    path('project/create/', create_project, name='create_project'),
    path('project/<int:project_id>/update/', update_project, name='update_project'),
    path('project/<int:project_id>/delete/', delete_project, name='delete_project'),
]