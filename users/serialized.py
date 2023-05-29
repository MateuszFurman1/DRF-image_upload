from django.forms import CharField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from Core import settings
from rest_framework.exceptions import ValidationError


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
        token['email'] = user.email
        token['user_id'] = user.id
        return token


User = settings.AUTH_USER_MODEL


class RegisterSerializer(ModelSerializer):
    password_confirmation = CharField(required=True)
    first_name = CharField(required=True)
    password = CharField(required=True)
    email = CharField(required=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'password', 'password_confirmation',
            'email'
        )

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise ValidationError({'error_message': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        user: User = User.objects.create(
            first_name=validated_data.get('first_name'),
            email=validated_data.get('email'),
        )

        user.set_password(validated_data.get('password'))
        user.save()

        return user