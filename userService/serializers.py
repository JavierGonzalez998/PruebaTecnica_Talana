from .models import User, Role
from .utils import encrypt_password
from rest_framework import serializers

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'password','email', 'role', 'created_at', 'updated_at']
        extra_kwargs = {
            'id': {'required': False, 'read_only': True},
            'password': {'write_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'required': False ,'read_only': True}
        }
    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = encrypt_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = encrypt_password(validated_data['password'])
        return super().update(instance, validated_data)
    