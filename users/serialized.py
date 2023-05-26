from dataclasses import field
from django.forms import CharField, EmailField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from users.models import CustomUser
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model


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
    password = CharField(write_only=True)
    password_confirmation = CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password_confirmation', 'first_name')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.pop('password_confirmation')

        if password != password_confirmation:
            raise ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirmation')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user
    # email = EmailField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    # )
    # password = CharField(
    #     required=True,
    #     validators=[validate_password]
    # )

    # class Meta:
    #     model = CustomUser
    #     fields = (
    #         'first_name', 'email',
    #         'password', 'password_confirmation',
    #     )

    # def validate(self, data):
    #     if data['password'] != data['password_confirmation']:
    #         raise ValidationError({'error_message': 'Passwords do not match'})
    #     return data

    # def create(self, validated_data):
    #     user: CustomUser = CustomUser.objects.create(
    #         email=validated_data.get('email'),
    #         first_name=validated_data.get('first_name'),
    #     )

    #     user.set_password(validated_data.get('password'))
    #     user.save()

    #     return user