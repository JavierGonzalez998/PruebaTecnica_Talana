from django.urls import path
from .views import Login, Register, Logout, UserInfo, UserEditProfile
from rest_framework_simplejwt.views import TokenRefreshView

# api/v1/game/
urlpatterns = [
    path('', UserInfo.as_view(), name='user'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', Logout.as_view(), name='logout'),
    path('edit/', UserEditProfile.as_view(), name='user_edit'),
]