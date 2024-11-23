from rest_framework import serializers
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