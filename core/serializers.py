from rest_framework import serializers
from .models import User,Job
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'], 
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            nin=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user

  class Meta:
    model = User
    fields = ["id", "first_name", "last_name", "email","phone_number", "nin","password"]
    


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

    