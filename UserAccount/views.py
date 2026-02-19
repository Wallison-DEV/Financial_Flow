from rest_framework import viewsets, permissions

from .models import UserModel, ProfileModel
from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsOwner

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwner]

    def get_queryset(self):
        return UserModel.objects.filter(id=self.request.user.id)

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner] 

    def get_queryset(self):
        return ProfileModel.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
