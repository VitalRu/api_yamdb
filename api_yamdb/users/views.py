from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ErrorDetail
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import UserAdminSerializer, UserSerializer
from .utility import get_tokens_for_user, send_code
from api.permissions import IsAdmin


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Регистрирует нового пользователя.
    """
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        if serializer.errors == {
            'username': [
                ErrorDetail(
                    string='A user with that username already exists.',
                    code='unique')
            ],
            'email': [
                ErrorDetail(
                    string='user with this email already exists.',
                    code='unique')
            ]
        }:
            user = User.objects.get(username=request.data['username'])
            token = default_token_generator.make_token(user)
            send_code(token, request.data['email'])
            return Response(request.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    token = default_token_generator.make_token(user)
    send_code(token, request.data['email'])
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """
    Получает JWT-токен для пользователя.
    """
    if (
            'username' not in request.data
            or 'confirmation_code' not in request.data
    ):
        return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)
    username = request.data['username']
    confirmation_code = request.data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, confirmation_code):
        return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)

    return Response(get_tokens_for_user(user), status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    Обеспечивает CRUD-операции для пользователей (администраторская роль).

    """
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']


class UserView(generics.RetrieveUpdateAPIView):
    """
    Отображает и обновляет информацию о текущем пользователе.

    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
