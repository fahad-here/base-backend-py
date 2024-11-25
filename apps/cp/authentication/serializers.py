from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

Customer = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, min_length=8)
  
  class Meta:
    model = Customer
    fields = ['email', 'password', 'first_name', 'last_name', 'phone', 'country']
  
  def create(self, validated_data):
    password = validated_data.pop('password')
    user = Customer(**validated_data)
    user.set_password(password)
    user.save()
    return user

class LoginSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField()

  def validate(self, attrs):
    user = authenticate(
        email=attrs.get('email'),
        password=attrs.get('password')
    )
    
    if not user:
        raise ValidationError('Invalid credentials')
    
    if not user.is_active:
        raise ValidationError('Account is disabled')
        
    attrs['user'] = user
    return attrs

class CustomerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Customer
    fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'country', 'status']
    read_only_fields = ['id', 'email', 'status']