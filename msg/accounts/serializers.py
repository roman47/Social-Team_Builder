from django.contrib.auth import get_user_model

from rest_framework import serializers
from . import models



class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'age',
            'gender',
            'size'
        )
        model = models.UserPref

    def create(self, validated_data):
        user = self.context['request'].user
        userpref = models.UserPref.objects.create(
            user=user,
            **validated_data
        )
        return userpref
