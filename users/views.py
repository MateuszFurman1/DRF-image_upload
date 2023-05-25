from rest_framework_simplejwt.views import TokenObtainPairView
from users.serialized import MyTokenObtainPairSerializer
from rest_framework.generics import CreateAPIView


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    pass