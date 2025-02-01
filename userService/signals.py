from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Role, User
from .serializers import UserSerializer
@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    # Lista de roles predeterminados
    default_roles = ["Admin", "User"]

    # Verifica si hay roles en la tabla
    if not Role.objects.exists():
        for role in default_roles:
            Role.objects.create(name=role)
        print("Roles predeterminados creados.")

@receiver(post_migrate)
def create_admin(sender, **kwargs):
    if not User.objects.exists():
        role = Role.objects.filter(name='Admin').first()
        userData = {
            "name": "test",
            "email": "test@test.com",
            "username": "userAdmin",
            "password": "test123123",
            "role": role.id,
        }
        serializer = UserSerializer(data = userData)
        if(serializer.is_valid()):
            serializer.save()