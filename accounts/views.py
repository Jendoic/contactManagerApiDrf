from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView

from .serializers import *
from .models import *


class TestApi(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    
    def get(self, request, *args, **kwargs):
        return Response({'message': 'User is authenticated'})
    

class SignUpView(generics.GenericAPIView):
    
    def post(self, request, *args, **kwargs):
        serializers = UserSerializer(data=request.data)
        
        data = {}
        
        if serializers.is_valid():
            account = serializers.save()
            data['response'] = 'successfully registered'
            data['email'] = account.email
            data['username'] = account.username
            
        else:
            data = serializers.errors
        
        return Response(data)
    
    
class LogOutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)