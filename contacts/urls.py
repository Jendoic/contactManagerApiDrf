from django.urls import path
from .views import *



urlpatterns = [
    path('contactlist/', ContactList.as_view(), name="contact-list"),
    path('contactdetails/<int:pk>/', ContactDetails.as_view(), name="contact-details"),
]
