from django.contrib.auth.models import User
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework import serializers
import re

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'},  write_only=True)
    
    
    class Meta:
        ref_name = 'accountSerializer'
        model = User
        
        fields = ('id', 'username', 'email', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}
        
        
        def validate_password(self, value):
            if len(value) < 6:
                raise serializers.ValidationError(
                    "Password must be at least 6 characters long"
                )
            if not re.search(r'[A-Z]', value):
                raise serializers.ValidationError(
                    "Password must contain at least one uppercase letter"
                )
            if not re.search(r'[a-z]', value):
                raise serializers.ValidationError(
                    "Password must contain at least one lowercase letter"
                )
            if not re.search(r'[0-9!@#$%]', value):
                raise serializers.ValidationError(
                    "Password must contain at least one number or special character"
                )
            return value
        
        # def validate_email(self, value):
        #     if User.objects.filter(email=value).exists():
        #         raise serializers.ValidationError(
        #             "This email address is already in use"
        #         )
        #     return value
        
        def save(self):
            password = self.validated_data['password']
            connfirm_password = self.validated_data['confirm_password']
            if password != connfirm_password:
                raise serializers.ValidationError(
                    "Passwords do not match"
                )
                
            if User.objects.filter(email=self.validated_data['email']).exists():
                raise serializers.ValidationError(
                    "This email address is already in use"
                )
                
            account = User(email=self.validated_data['email'], username=self.validated_data['username'])
            account.set_password(password)
            account.save()
            return account