from rest_framework import serializers

from . import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.User
        fields = ['url', 'id', 'username']

class SampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Sample
        fields = ['url', 'id', 'user', 'timestamp', 'values']
