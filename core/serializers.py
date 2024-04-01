from rest_framework import serializers
from .models import User,Job,NewsLetterSubscriberModel
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from payment.serializers import PaymentSerializer


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields="__all__"
        extra_kwargs = {'user': {'read_only': True}}
        
    def create(self, validated_data):
        user = self.context['userinfo']  # Get user from request
        job = Job.objects.create(**validated_data, user=user)
        return job
        
        
        
class UserSerializer(serializers.ModelSerializer):
    job = JobSerializer(many=True, read_only=True)
    payment=PaymentSerializer(many=True, read_only=True)
    class Meta:
      model = User
      fields = ["id", "first_name","last_name", "email","phone_number", "nin","password", "job", "user_type", "payment"]
      extra_kwargs = {'password': {'write_only': True}}
      
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



      
    

class NewsLetterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetterSubscriberModel
        fields="__all__"