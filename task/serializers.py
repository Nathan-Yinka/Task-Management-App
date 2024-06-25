from datetime import datetime

from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.utils import DateValidationUtility

User = get_user_model()

from .models import Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", 'username']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_due_date(self, value):
        return value.strftime('%Y-%m-%d %H:%M:%S.%f')
    
    def validate_category(self, value):
        category = value.lower().strip()
        return category
    
    def validate_title(self, value):
        title = value.strip()
        return title

class TaskReadSerializer(serializers.ModelSerializer):
    formatted_due_date = serializers.SerializerMethodField(read_only=True)
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

            
    def get_formatted_due_date(self, obj):
        return obj.get_formatted_due_date()