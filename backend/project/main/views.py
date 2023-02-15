from django.shortcuts import render
from rest_framework import viewsets

from . import serializers, models

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class SampleViewSet(viewsets.ModelViewSet):
    queryset = models.Sample.objects.all()
    serializer_class = serializers.SampleSerializer
