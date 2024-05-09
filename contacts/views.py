from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .serializers import UserSerializer, ContactSerializer
from .models import Contact


class ContactList(generics.ListCreateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)
    
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
    
    
class ContactDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[permissions.IsAuthenticated]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
    
    # def get_queryset(self, *args, **kwargs):
    #     contact_id = self.kwargs['pk']
    #     contact = Contact.objects.filter(pk=contact_id)
        
    #     if self.request.user != contact.user:
    #         raise PermissionDenied(
    #             "Contact Not Found"
    #         )
    
    
    def perform_update(self, serializer):
        contact = self.get_object()
        
        if self.request.user != contact.user:
            raise PermissionDenied(
                "You are not allowed to edit this contact"
            )
            
        serializer.save()
        
        
    def perform_destroy(self, instance): 
        if self.request.user != instance.user:
            raise PermissionDenied(
                "You are not allowed to delete this contact"
            )
        instance.delete()