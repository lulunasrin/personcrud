from rest_framework import serializers
from .models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person  # Specify the model to be serialized
        fields = ['id', 'name', 'age', 'location']  # Specify the fields to be included in the serialized output
