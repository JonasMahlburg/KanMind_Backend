from rest_framework import generics
from user_auth_app.models import UserProfile
from .serializers import RegistrationSerializer, EmailAuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


"""
API view to list all user profiles or create a new user profile.
Uses the RegistrationSerializer to handle user profile data.
"""
class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = RegistrationSerializer

"""
API view to retrieve, update, or delete a specific user profile by ID.
Uses the RegistrationSerializer to manage user profile operations.
"""
class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = RegistrationSerializer

"""
API view to register a new user.
If registration is successful, a token is created and returned with user data.
If the user already exists or the data is invalid, the errors are returned.
"""
class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()
            token, create = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'fullname': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id

            }
        else:
            data=serializer.errors
        
        return Response(data)


"""
API view for user login using token authentication.
If credentials are valid, returns an authentication token and user information.
Otherwise, returns validation errors.
"""



class CustomLogInView(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = EmailAuthTokenSerializer  

    def post(self, request):
        serializer = self.serializer_class(data={
            'email': request.data.get('email'),
            'password': request.data.get('password')
        })

        data = {}

        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, create = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'fullname': user.username,
                'email': user.email,
                'user_id': user.id
            }
        else:
            data=serializer.errors
        
        return Response(data)