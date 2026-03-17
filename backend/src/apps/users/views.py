from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from apps.core.permissions import GroupPermission
from .models import User
from .serializers import UserCreateSerializer, UserDetailSerializer, UserUpdateSerializer, UserListSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_resource = 'users'
    permission_classes = [IsAuthenticated, GroupPermission]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'created_at']
    serializer_classes = {
        'create': UserCreateSerializer,
        'list': UserListSerializer,
        'retrieve': UserDetailSerializer,
        'update': UserUpdateSerializer,
        'partial_update': UserUpdateSerializer,
    }
    serializer_class = UserListSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        return Response(UserListSerializer(request.user).data)
