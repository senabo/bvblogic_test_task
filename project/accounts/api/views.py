from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)

from .permissions import IsOwnerOrReadOnly
from .serializer import CreateProfileSerializer, UpdateProfileSerializer
from accounts.models import UserProfile

User = get_user_model()


class CreateProfileView(generics.CreateAPIView):
    """Create new user profile"""

    queryset = User.objects.all()
    serializer_class = CreateProfileSerializer
    permission_classes = (AllowAny,)


class UpdateProfileView(generics.RetrieveUpdateAPIView):
    """Show or update user profile"""

    queryset = User.objects.all()
    serializer_class = UpdateProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    lookup_field = "username"
