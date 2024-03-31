from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from  .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields="__all__"
        extra_kwargs = {'user': {'read_only': True}}
        
    def create(self, validated_data):
        user = self.context['userinfo']  # Get user from request
        payment = Payment.objects.create(**validated_data, user=user)
        return  payment
    
        
        
