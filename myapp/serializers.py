from rest_framework import serializers
from .models import Person
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


from rest_framework import serializers
from .models import UserNew

class RegisterUserNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNew
        fields = ['name', 'email', 'phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = UserNew.objects.create_user(
            email=validated_data['email'],
            phone=validated_data['phone'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise serializers.ValidationError("Email is required")
        if not password:
            raise serializers.ValidationError("Password is required")

        # Authenticate using the email field
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user
        return data
    
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person  # Specify the model to be serialized
        fields = ['id', 'name', 'age', 'location']  # Specify the fields to be included in the serialized output
