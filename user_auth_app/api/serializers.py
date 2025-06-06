from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



"""
Serializer for the UserProfile model.
Handles serialization and deserialization of user profile data, including user, bio, and location.
"""
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']


"""
Serializer for user registration.
Validates that passwords match and that the email is unique before creating a new User instance.
"""
class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True, allow_blank=False)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    """
    Custom save method to create a new User instance after validating passwords and email uniqueness.
    """
    def save(self):
        pw = self.validated_data.pop('password')
        repeated_pw = self.validated_data.pop('repeated_password')
        fullname = self.validated_data.pop('fullname')

        if pw != repeated_pw:
            raise serializers.ValidationError({'error': 'Passwords do not match'})

        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'This email is already taken'})

        base_username = fullname.strip().replace(" ", "").lower()
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        account = User(
            email=self.validated_data['email'],
            username=username,
            first_name=fullname  # oder splitten, falls du Vor-/Nachname willst
        )
        account.set_password(pw)
        account.save()
        return account






class EmailCheckView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'No user with this email found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'id': user.id,
            'email': user.email,
            'fullname': user.username
        }, status=status.HTTP_200_OK)
    


class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email", write_only=True)
    password = serializers.CharField(label="Password", style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid email or password.")

            user = authenticate(self.context.get('request'), username=user.username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        attrs['user'] = user
        return attrs