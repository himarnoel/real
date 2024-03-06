from rest_framework import serializers
from .models import User,Job,NewsLetterSubscriberModel
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields="__all__"
        extra_kwargs = {'user': {'read_only': True}}
        
    def create(self, validated_data):
        user = self.context['request'].user  # Get user from request
        job = Job.objects.create(**validated_data, user=user)
        return job
        
        
        
class UserSerializer(serializers.ModelSerializer):
    job = JobSerializer(many=True, read_only=True)
    class Meta:
      model = User
      fields = ["id", "first_name","last_name", "email","phone_number", "nin","password", "job"]
      extra_kwargs = {'password': {'write_only': True}}
      
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'], 
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            nin=validated_data['nin'],
            password=validated_data['password']
        )
        return user
  



class NewsLetterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetterSubscriberModel
        fields="__all__"