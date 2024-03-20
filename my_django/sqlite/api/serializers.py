from rest_framework import serializers
from .models import PathChecker


class PathSerializer(serializers.ModelSerializer):
    class Meta:
        model = PathChecker
        fields = ["id", "title", "path"]