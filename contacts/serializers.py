from rest_framework import serializers
from .models import Contact
from django.contrib.auth.models  import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        

class ContactSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Contact
        fields = ('id', 'name', 'email', 'phone', 'user')
        