from django.urls import path

from adminka.views.app_reviews_views import *
from adminka.views.applications_views import *
from adminka.views.directions_views import *
from adminka.views.efficiencies_views import *
from adminka.views.profiles_views import *
from adminka.views.projects_views import *
from adminka.views.skills_views import *
from adminka.views.teams_views import *
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


    path('directions/', get_all_directions, name='get_all_directions'),
    path('directions/<int:direction_id>/', get_direction_by_id, name='get_direction_by_id'),
    path('directions/create/', create_direction, name='create_direction'),
    path('directions/<int:direction_id>/update/', update_direction, name='update_direction'),
    path('directions/<int:direction_id>/delete/', delete_direction, name='delete_direction'),


    path('teams/', get_all_teams, name='get_all_teams'),
    path('teams/<int:team_id>/', get_team_by_id, name='get_team_by_id'),
    path('teams/create/', create_team, name='create_team'),
    path('teams/<int:team_id>/update/', update_team, name='update_team'),
    path('teams/<int:team_id>/delete/', delete_team, name='delete_team'),


    path('applications/', get_all_applications, name='get_all_applications'),
    path('applications/<int:application_id>/', get_application_by_id, name='get_application_by_id'),
    path('applications/create/', create_application, name='create_application'),
    path('applications/<int:application_id>/update/', update_application, name='update_application'),
    path('applications/<int:application_id>/delete/', delete_application, name='delete_application'),

    path('app_reviews/', get_all_reviews, name='get_all_reviews'),
    path('app_reviews/<int:review_id>/', get_review_by_id, name='get_review_by_id'),
    path('app_reviews/create/', create_review, name='create_review'),
    path('app_reviews/<int:review_id>/update/', update_review, name='update_review'),
    path('app_reviews/<int:review_id>/delete/', delete_review, name='delete_review'),

]