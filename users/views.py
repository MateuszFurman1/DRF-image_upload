from rest_framework_simplejwt.views import TokenObtainPairView
from Core import settings
from users import serialized
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken



User = settings.AUTH_USER_MODEL


class UserRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'ErrorDetail' in str(data):
            response = {'errors': data}
        else:
            response = data

        return super().render(response, accepted_media_type, renderer_context)


class LoginView(TokenObtainPairView):
    serializer_class = serialized.MyTokenObtainPairSerializer
    permission_classes = [AllowAny]



def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class RegisterView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = serialized.RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.create(serializer.validated_data)
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
 

# class RegisterView(CreateAPIView):
    
#     permission_classes = [AllowAny]
#     serializer_class = serialized.RegisterSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         # user = serializer.save()
#         # token = RefreshToken.for_user(user)
#         # data = serializer.data
#         # data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
#         # return Response(data, status=status.HTTP_201_CREATED)

#         user = serializer.create(
#             validated_data=serializer.validated_data)
#         refresh = serialized.MyTokenObtainPairSerializer.get_token(user)

#         return Response({
#             'refresh': (refresh),
#             'access': (refresh.access_token)
#         }, status=status.HTTP_201_CREATED)

        
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
  
    def post(self, request, format=None):
        serializer = serialized.ProfileSerializer(data=request.user)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
    
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
        serializer.save()

        return Response({'detail': 'Password reset link sent. Please check your email.'},
            status=status.HTTP_200_OK)
        
        
class PasswordResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, uid, token, format=None):
        serializer = serialized.PasswordResetSerializer(
            data=request.data,
            context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Password reset successfully'},
            status=status.HTTP_200_OK)