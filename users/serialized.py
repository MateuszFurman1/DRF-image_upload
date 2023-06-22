from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
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


class RegisterSerializer(ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'email', 'password', 'password_confirmation'
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
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
    
    
class UserChangePasswordSerializer(serializers.Serializer):
    password_confirmation = serializers.CharField(write_only=True,
                                                style={'input_type':'password'}, required=True)
    class Meta:
        fields = ['password', 'password_confirmation']
    
    def validate(self, data):
        user = self.context.get('user')
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError('Passwords do not match')
        user.set_password(data.get('password'))
        user.save()
        return data