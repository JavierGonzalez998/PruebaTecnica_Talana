from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Role
from .serializers import UserSerializer
from .utils import check_password, get_user_id_from_request
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated, AllowAny

class Login(APIView):
    def post(self, request):
        body = request.data
        email = body.get("email", None)
        password = body.get("password", None)
        if not email or not password:
            return Response({'error': 'email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        password_valid = check_password(password, user.password) if user else False
        if not password_valid:
            return Response({'error': 'email or password invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "status": 200,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": user.role.name
        }, status=status.HTTP_200_OK)
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return super().get_permissions()

class Register(APIView):
    def post(self, request):
        body = request.data
        role = Role.objects.filter(name='User').first()

        if not role:
            return Response({'error': 'role not found'}, status=status.HTTP_404_NOT_FOUND)
        
        body['role'] = role.id
        serializer = UserSerializer(data=body)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":200, "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return super().get_permissions()

class UserEditProfile(APIView):
    def patch(self, request):
        id = get_user_id_from_request(request)
        user = User.objects.filter(pk=id).first()
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 200,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({'error': 'los datos no son válidos'}, status=status.HTTP_418_IM_A_TEAPOT)
    def get_permissions(self):    
        if self.request.method == 'PATCH':
            return [IsAuthenticated()]
        return super().get_permissions()

class Logout(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()  # Invalida el token
            return Response({"status":200,"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):    
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return super().get_permissions()


class UserInfo(APIView):
    def get(self, request):
        id = get_user_id_from_request(request)
        user = User.objects.filter(pk=id).first()
        if not user:
            return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return super().get_permissions()
