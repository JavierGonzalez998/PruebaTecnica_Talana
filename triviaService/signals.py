from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Difficulty

@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    # Lista de roles predeterminados
    default_difficulty = ["Facil", "Medio", "Dificil"]

    # Verifica si hay roles en la tabla
    if not Difficulty.objects.exists():
        for difficulty in default_difficulty:
            Difficulty.objects.create(name=difficulty)
        print("Dificultades creadas.")