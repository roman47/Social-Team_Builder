from django.contrib.auth import get_user_model

from rest_framework import serializers
from . import models



class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'skill_name',
        )
        model = models.Skills


