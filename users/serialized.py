from base64 import urlsafe_b64decode
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.utils.encoding import smart_str
from users.models import CustomUser


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
        token['email'] = user.email
        token['user_id'] = user.id
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'email', 'password', 'password_confirmation')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Passwords do not match')
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create(
            first_name=validated_data.get('first_name'),
            email=validated_data.get('email'),
        )

        user.set_password(validated_data.get('password'))
        user.save()

        return user
    
    
class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ('first_name', 'email')
    
    
class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password_confirmation = serializers.CharField(write_only=True, style={'input_type':'password'}, required=True)
    
    class Meta:
        fields = ['password', 'password_confirmation']
    
    def create(self, data):
        user = self.context.get('user')
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Passwords do not match')
        if user.check_password(data.get('password')) or user.check_password(data.get('password_confirmation')):
            raise serializers.ValidationError('Passwords are the same as old one')
        user.set_password(data.get('password'))
        user.save()
        return data   
    

class SendPasswordResetEmailSerializer(serializers.Serializer):  # noqa: E999
    email = serializers.EmailField(max_length=255)

    def validate(self, data):
        email = data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('You are not a registered user.')

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        reset_link = f'http://localhost:3000/api/user/reset/{uid}/{token}'

        # Send email
        subject = 'Reset Your Password'
        body = f'Click the following link to reset your password: {reset_link}'
        to_email = user.email

        send_mail(subject, body, 'sender@example.com', [to_email], fail_silently=False)

        return data


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password_confirmation = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        uid = self.context.get('uid')
        token = self.context.get('token')

        if password != password_confirmation:
            raise serializers.ValidationError("Password and Confirm Password don't match")

        try:
            user_id = smart_str(urlsafe_b64decode(uid))
            user = CustomUser.objects.get(id=user_id)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError('Invalid user ID')

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError('Token is not valid or expired')

        user.set_password(password)
        user.save()

        return data
