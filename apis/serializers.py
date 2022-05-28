# apis/serializers.py
from rest_framework import serializers, fields
from todos import models
from django.utils import timezone


class TodoSerializer(serializers.ModelSerializer):
    due_date = serializers.DateTimeField(
        default=timezone.now, format="%Y-%m-%d")

    class Meta:
        fields = (
            'id',
            'title',
            'description',
            'due_date',
            'tag',
            'status',
        )
        model = models.Todo
