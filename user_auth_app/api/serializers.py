from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User

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

    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    """
    Custom save method to create a new User instance after validating passwords and email uniqueness.
    """
    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError({'error':'passwords dont match'})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
             raise serializers.ValidationError({'error':'this Email is already taken'})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()
        return account