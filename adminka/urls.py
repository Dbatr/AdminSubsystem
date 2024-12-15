from django.urls import path

from adminka.views.app_reviews_views import *
from adminka.views.applications_views import *
from adminka.views.check_list_items_views import *
from adminka.views.comments_views import *
from adminka.views.customization_views import *
from adminka.views.directions_views import *
from adminka.views.efficiencies_views import *
from adminka.views.grades_views import *
from adminka.views.profiles_views import *
from adminka.views.projects_views import *
from adminka.views.results_views import *
from adminka.views.roles_views import *
from adminka.views.skills_views import *
from adminka.views.status_views import *
from adminka.views.tags_views import *
from adminka.views.tasks_views import *
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
    path('profile/get_role/', RoleByTokenView.as_view(), name='get_role'),


    path('roles/assign/', assign_role_to_user, name='assign_role_to_user'),
    path('roles/', get_all_roles, name='get_all_roles'),
    path('roles/<int:role_id>/', get_role_by_id, name='get_role_by_id'),
    path('roles/create/', create_role, name='create_role'),
    path('roles/<int:role_id>/delete/', delete_role, name='delete_role'),
    path('roles/valid-options/', get_valid_roles, name='get_valid_roles'),


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
    path('teams/me_curator/', get_curator_teams, name='get_curator_teams'),


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


    path('tasks/', get_all_tasks, name='get_all_tasks'),
    path('tasks/<int:task_id>/', get_task_by_id, name='get_task_by_id'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:task_id>/update/', update_task, name='update_task'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),


    path('checklist/', get_all_checklist_items_global, name='get_all_checklist_items_global'),
    path('tasks/<int:task_id>/checklist/', get_all_checklist_items, name='get_all_checklist_items'),
    path('tasks/<int:task_id>/checklist/<int:item_id>/', get_checklist_item_by_id,
         name='get_checklist_item_by_id'),
    path('tasks/checklist/create/', create_checklist_item, name='create_checklist_item'),
    path('tasks/checklist/<int:item_id>/update/', update_checklist_item,
         name='update_checklist_item'),
    path('tasks/<int:task_id>/checklist/<int:item_id>/delete/', delete_checklist_item,
         name='delete_checklist_item'),


    path('customizations/', get_all_customizations, name='get_all_customizations'),
    path('customizations/task/<int:task_id>/', get_customizations_by_task, name='get_customizations_by_task'),
    path('customizations/create/', create_customization, name='create_customization'),
    path('customizations/<int:customization_id>/update/', update_customization, name='update_customization'),
    path('customizations/<int:customization_id>/delete/', delete_customization, name='delete_customization'),

    path('statuses/', get_all_statuses, name='get_all_statuses'),
    path('statuses/direction/<int:direction_id>/', get_statuses_by_direction, name='get_statuses_by_direction'),
    path('statuses/create/', create_status, name='create_status'),
    path('statuses/update/<int:status_id>/', update_status, name='update_status'),
    path('statuses/delete/<int:status_id>/', delete_status, name='delete_status'),

    path('tags/', get_all_tags, name='get_all_tags'),
    path('tags/task/<int:task_id>/', get_tags_by_task, name='get_tags_by_task'),
    path('tags/create/', create_tag, name='create_tag'),
    path('tags/update/<int:tag_id>/', update_tag, name='update_tag'),
    path('tags/delete/<int:tag_id>/', delete_tag, name='delete_tag'),
    path('tags/<str:tag_name>/tasks/', get_tasks_by_tag_name, name='tasks_by_tag_name'),


    path('results/', get_all_results, name='get_all_results'),
    path('results/<int:result_id>/', get_result_by_id, name='get_result_by_id'),
    path('results/create/', create_result, name='create_result'),
    path('results/<int:result_id>/update/', update_result, name='update_result'),
    path('results/<int:result_id>/delete/', delete_result, name='delete_result'),


    path('grades/', get_all_grades, name='get_all_grades'),
    path('grades/<int:grade_id>/', get_grade_by_id, name='get_grade_by_id'),
    path('grades/create/', create_grade, name='create_grade'),
    path('grades/<int:grade_id>/update/', update_grade, name='update_grade'),
    path('grades/<int:grade_id>/delete/', delete_grade, name='delete_grade'),


    path('comments/', get_all_comments, name='get_all_comments'),
    path('comments/task/<int:task_id>/', get_comments_by_task, name='get_comments_by_task'),
    path('comments/create/', create_comment, name='create_comment'),
    path('comments/<int:comment_id>/update/', update_comment, name='update_comment'),
    path('comments/<int:comment_id>/delete/', delete_comment, name='delete_comment'),

]