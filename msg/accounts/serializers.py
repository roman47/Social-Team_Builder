from django.contrib.auth import get_user_model

from rest_framework import serializers
from . import models


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'skill_name',
        )
        model = models.Skill


