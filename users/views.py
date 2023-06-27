from rest_framework_simplejwt.views import TokenObtainPairView
from Core import settings
from users import serialized
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


User = settings.AUTH_USER_MODEL

class LoginView(TokenObtainPairView):
    serializer_class = serialized.MyTokenObtainPairSerializer
    permission_classes = [AllowAny]



class RegisterView(CreateAPIView):
    serializer_class = serialized.RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.create(
            validated_data=serializer.validated_data
        )
        refresh = serialized.MyTokenObtainPairSerializer.get_token(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
        
        
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
  
    def get(self, request, format=None):
        serializer = serialized.ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = serialized.ChangePasswordSerializer(
            data=request.data,
            context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
    
        return Response({'detail': 'Password changed successfully'},
                    status=status.HTTP_200_OK)
        

class SendPasswordResetEmailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = serialized.SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_reset_email()

        return Response({'detail': 'Password reset link sent. Please check your email.'},
            status=status.HTTP_200_OK)
        
        
class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, uid, token, format=None):
        serializer = serialized.UserPasswordResetSerializer(
            data=request.data,
            context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        serializer.reset_password()

        return Response({'detail': 'Password reset successfully'},
            status=status.HTTP_200_OK)