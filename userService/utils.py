import bcrypt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
from rest_framework import status
from .models import User

def encrypt_password(password:str)->str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password:str, hashed:str)->bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def get_user_id_from_request(request):
    auth = JWTAuthentication()
    header = auth.get_header(request)
    raw_token = auth.get_raw_token(header)

    if raw_token is None:
        return {"error": "No token provided"}
    try:
        validated_token = auth.get_validated_token(raw_token)
        payload = validated_token.payload
        return payload['user_id']
    except TokenError as e:
        return {"error": str(e)}
    except InvalidToken as e:
        return {"error": str(e)}
    
def validate_user(request):
    userid = get_user_id_from_request(request)
    user = User.objects.filter(pk=userid).first()
    if not user:
        return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
    return user
    
def validate_admin(request):
    id = get_user_id_from_request(request)
    user = User.objects.filter(pk=id).first()
    if not user:
        return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
    if int(user.role.id) != 1:
        return Response({'error': 'user is not an admin'}, status=status.HTTP_401_UNAUTHORIZED)
    return user