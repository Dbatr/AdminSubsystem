from rest_framework import serializers

from canban.models import *
from crm.models import *


class SimpleRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        # Создание пользователя
        username = validated_data['username']
        password = validated_data['password']
        user = User.objects.create_user(username=username, password=password)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['author', 'photo', 'telegram', 'email', 'surname', 'name', 'patronymic', 'course', 'university', 'skills']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'date_joined']


class EfficiencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Efficiency
        fields = ['user', 'count', 'rating']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'author', 'supervisor', 'curators', 'students', 'link', 'start', 'end']


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class AppReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = App_review
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = '__all__'


class CustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customization
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'direction', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'task', 'name']