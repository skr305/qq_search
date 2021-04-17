from django.urls import path
from weapon.views import get_weapon_info

weapon_patterns = [
    path('', get_weapon_info),
]