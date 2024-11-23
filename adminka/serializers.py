from rest_framework import serializers
from crm.models import *


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['author', 'photo', 'telegram', 'email', 'surname', 'name', 'patronymic', 'course', 'university', 'skills']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']