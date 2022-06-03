# apis/serializers.py
from rest_framework import serializers, fields
from todos import models
import datetime


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ('id', 'name')


class TodoSerializer(serializers.ModelSerializer):
   # tags = TagSerializer(many=True, read_only=True)
    tags = serializers.SlugRelatedField(
        many=True, slug_field='name', queryset=models.Tag.objects.all())
    depth = 1

    def validate_date(due_date):
        if due_date < datetime.date.today():
            raise serializers.ValidationError("Date cannot be in the past")

    due_date = serializers.DateField(validators=[validate_date],
                                     format="%Y-%m-%d")

    def getUsername(self, obj):
        return obj.user.username

    username = serializers.SerializerMethodField('getUsername')

    class Meta:
        model = models.Todo
        fields = ('id', 'title', 'description', 'due_date',
                  'tags', 'status', 'username', 'timestamp')
