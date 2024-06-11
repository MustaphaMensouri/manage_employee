from rest_framework import serializers
from .models import Ferme

class FermeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ferme
        fields = ['id', 'name', 'address', 'capital']


