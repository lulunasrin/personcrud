
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



#class based
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserNew
from .serializers import RegisterUserNewSerializer,LoginSerializer
from .serializers import PersonSerializer

class RegisterUserNewAPI(APIView):
    permission_classes = [] 
    def post(self, request):
        serializer = RegisterUserNewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    permission_classes = []  # No authentication required for login

    def post(self, request):
        _data = request.data
        serializer = LoginSerializer(data=_data)

        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'login successful',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)




class PersonView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def print_user_name(self, request):
        # Print the authenticated user's name
        if request.user.is_authenticated:
            print(request.user.name)

    def get(self, request):
        self.print_user_name(request)  # Print user name

        # Retrieve all Person objects
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    def post(self, request):
        self.print_user_name(request)  # Print user name

        # Create a new Person object
        serializer = PersonSerializer(data=request.data)

        if serializer.is_valid():
            if request.user.is_authenticated:
                if request.user.name == serializer.validated_data['name']:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"detail": "Permission denied. You cannot modify this user."},
                                    status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({"detail": "Authentication credentials were not provided."},
                                status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        self.print_user_name(request)  # Print user name

        # Update an existing Person object
        try:
            person = Person.objects.get(id=request.data['id'])
        except Person.DoesNotExist:
            return Response({"error": "Person not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the authenticated user matches the person being updated
        if request.user.is_authenticated:
            if request.user.name == person.name:
                serializer = PersonSerializer(person, data=request.data, partial=False)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Permission denied. You cannot modify this user."},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        self.print_user_name(request)  # Print user name

        # Partially update an existing Person object
        try:
            person = Person.objects.get(id=request.data['id'])
        except Person.DoesNotExist:
            return Response({"error": "Person not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the authenticated user matches the person being updated
        if request.user.is_authenticated:
            if request.user.name == person.name:
                serializer = PersonSerializer(person, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "Permission denied. You cannot modify this user."},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        self.print_user_name(request)  # Print user name

        # Delete a Person object
        try:
            person = Person.objects.get(id=request.data['id'])
        except Person.DoesNotExist:
            return Response({"error": "Person not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the authenticated user matches the person being deleted
        if request.user.is_authenticated:
            if request.user.name == person.name:
                person.delete()
                return Response({"message": "Person deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "Permission denied. You cannot delete this user."},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)





@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        # Retrieve all Person objects
        objPerson = Person.objects.all()
        serializer = PersonSerializer(objPerson, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new Person object
        data = request.data
        serializer = PersonSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'PUT':
        # Update an existing Person object
        data = request.data
        try:
            obj = Person.objects.get(id=data['id'])
        except Person.DoesNotExist:
            return Response({"error": "Person not found"}, status=404)

        serializer = PersonSerializer(obj, data=data, partial=False)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'PATCH':
        # Partially update an existing Person object
        data = request.data
        try:
            obj = Person.objects.get(id=data['id'])
        except Person.DoesNotExist:
            return Response({"error": "Person not found"}, status=404)

        serializer = PersonSerializer(obj, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        # Delete a Person object
        data = request.data
        try:
            obj = Person.objects.get(id=data['id'])
        except Person.DoesNotExist:
            return Response({"error": "Person not found"}, status=404)

        obj.delete()
        return Response({"message": "Person deleted successfully"}, status=204)
    








from rest_framework import viewsets
from .models import Person
from .serializers import PersonSerializer

class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()  # Define the queryset for the viewset
    serializer_class = PersonSerializer  # Specify the serializer to be used





























@api_view(['GET'])
def index(request):
    people_details = {
        "name": "sree",
        "age": 30
    }
    return Response(people_details)
